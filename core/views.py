import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect, render


from .models import (
    AboutChecklistItem,
    AboutHighlightCard,
    AboutIntro,
    AboutMissionVision,
    AboutServiceCard,
    AboutStat,
    AboutValueSection,
    AboutValueStep,
    AboutWhyCard,
    AboutWhySection,
    Banner,
    BenefitCard,
    BenefitsSection,
    CareerHero,
    ContactLocation,
    ContactPageInfo,
    ContactSubmission,
    CultureCard,
    CultureSection,
    FAQ,
    HomeAboutChecklistItem,
    HomeAboutSection,
    HomeHero,
    HomeProcessFrame,
    HomeProcessSection,
    HomeWhyCard, 
    HomeWhySection,
    HomeServiceCard,
    IndustryCard,
    JobOpening,
    LifeAtVISImage,
    LifeAtVISSection,
    OpenPositionsSection,
    ProductCard,
    ServiceCard,
    ServiceFeature,
    ServiceSolutionCard,
    SolutionCard,
    WorkingProcessStep,
)


def home(request):
    context = {
        "hero": HomeHero.objects.first(),
        "about_section": HomeAboutSection.objects.first(),
        "about_checklist": HomeAboutChecklistItem.objects.filter(is_active=True).order_by("order"),
        "stats": AboutStat.objects.filter(is_active=True).order_by("order"),
        "process_section": HomeProcessSection.objects.first(),
        "process_frames": HomeProcessFrame.objects.filter(is_active=True).order_by("order"),
        "home_service_cards": HomeServiceCard.objects.filter(is_active=True).order_by("order"),
        "home_why_section": HomeWhySection.objects.first(),
        "home_why_cards": HomeWhyCard.objects.filter(is_active=True).order_by("order"),
    }
    return render(request, "home.html", context)


def about(request):
    context = {
        "banner": Banner.objects.filter(page="about", is_active=True).first(),
        "intro": AboutIntro.objects.first(),
        "highlight_cards": AboutHighlightCard.objects.filter(is_active=True).order_by("order"),
        "checklist_items": AboutChecklistItem.objects.filter(is_active=True).order_by("order"),
        "stats": AboutStat.objects.filter(is_active=True).order_by("order"),
        "service_cards": AboutServiceCard.objects.filter(is_active=True).order_by("order"),
        "value_section": AboutValueSection.objects.first(),
        "value_steps": AboutValueStep.objects.filter(is_active=True).order_by("order"),
        "mission_vision_cards": AboutMissionVision.objects.filter(is_active=True).order_by("order"),
        "why_section": AboutWhySection.objects.first(),
        "why_cards": AboutWhyCard.objects.filter(is_active=True).order_by("order"),
    }
    return render(request, "about.html", context)


def services(request):
    context = {
        "banner": Banner.objects.filter(page="services", is_active=True).first(),
        "service_cards": ServiceCard.objects.filter(is_active=True).order_by("order"),
        "process_steps": WorkingProcessStep.objects.filter(is_active=True).order_by("order"),
        "industry_cards": IndustryCard.objects.filter(is_active=True).order_by("order"),
    }
    return render(request, "services.html", context)


def our_products(request):
    cards = list(ProductCard.objects.filter(is_active=True).order_by("order"))
    context = {
        "banner": Banner.objects.filter(page="our_products", is_active=True).first(),
        "stats": AboutStat.objects.filter(is_active=True).order_by("order"),
        "featured_card": cards[0] if cards else None,
        "product_cards": cards[1:],
    }
    return render(request, "our_products.html", context)


def product_detail(request, slug):
    product = ProductCard.objects.filter(slug=slug, is_active=True).first()
    if not product:
        raise Http404("Product not found")

    context = {
        "banner": Banner.objects.filter(page="our_products", is_active=True).first(),
        "product": product,
        "gallery_images": product.gallery_images.filter(is_active=True).order_by("order"),
    }
    return render(request, "product_detail.html", context)


def solutions(request):
    context = {
        "banner": Banner.objects.filter(page="solutions", is_active=True).first(),
        "process_steps": WorkingProcessStep.objects.filter(is_active=True).order_by("order"),
        "solution_cards": SolutionCard.objects.filter(is_active=True).order_by("order"),
    }
    return render(request, "solutions.html", context)


def careers(request):
    context = {
        "hero": CareerHero.objects.first(),
        "open_positions_section": OpenPositionsSection.objects.first(),
        "jobs": JobOpening.objects.filter(is_active=True).order_by("order"),
        "life_section": LifeAtVISSection.objects.first(),
        "life_images": LifeAtVISImage.objects.filter(is_active=True).order_by("order"),
        "culture_section": CultureSection.objects.first(),
        "culture_cards": CultureCard.objects.filter(is_active=True).order_by("order"),
        "benefits_section": BenefitsSection.objects.first(),
        "benefit_cards": BenefitCard.objects.filter(is_active=True).order_by("order"),
    }
    return render(request, "careers.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        name_valid = bool(re.match(r"^[A-Za-z\s]+$", name)) if name else False
        phone_valid = bool(re.match(r"^[0-9]{10}$", phone)) if phone else True  # phone is optional

        email_valid = True
        if email:
            try:
                validate_email(email)
            except ValidationError:
                email_valid = False
        else:
            email_valid = False

        if name and email and message and name_valid and phone_valid and email_valid:
            ContactSubmission.objects.create(name=name, email=email, phone=phone, message=message)

            page_info = ContactPageInfo.objects.first()
            if page_info and page_info.company_email:
                try:
                    send_mail(
                        subject=f"New contact form message from {name}",
                        message=(
                            f"Name: {name}\n"
                            f"Email: {email}\n"
                            f"Phone: {phone}\n\n"
                            f"Message:\n{message}"
                        ),
                        from_email=None,
                        recipient_list=[page_info.company_email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

            messages.success(request, "Your message has been sent. We'll get back to you soon.")
            return redirect("home")
        elif not name_valid:
            messages.error(request, "Please enter a valid name using letters only.")
        elif not email_valid:
            messages.error(request, "Please enter a valid email address.")
        elif not phone_valid:
            messages.error(request, "Please enter a valid 10-digit mobile number.")
        else:
            messages.error(request, "Please fill in all required fields.")

    context = {
        "banner": Banner.objects.filter(page="contact", is_active=True).first(),
        "page_info": ContactPageInfo.objects.first(),
        "locations": ContactLocation.objects.filter(is_active=True).order_by("order"),
        "faqs": FAQ.objects.filter(is_active=True).order_by("order"),
    }
    return render(request, "contact.html", context)


def service_detail(request, slug):
    service = ServiceCard.objects.filter(slug=slug, is_active=True).first()
    if not service:
        raise Http404("Service not found")

    context = {
        "service": service,
        "solution_cards": service.solution_cards.filter(is_active=True).order_by("order"),
        "features": service.features.filter(is_active=True).order_by("order"),
    }
    return render(request, "service_detail.html", context)