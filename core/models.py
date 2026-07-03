from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    """
    Singleton model. Controls the site logo, title, and global contact
    details used in the header and footer. Only one row should ever exist —
    enforced in save() and in the admin (no "add" once one exists).
    """

    site_title = models.CharField(
        max_length=100,
        default="Vetri IT Systems Pvt Ltd",
        help_text="Shown in the header next to the logo, and in the browser tab.",
    )
    logo = models.ImageField(
        upload_to="site/",
        help_text="Header + footer logo. Transparent PNG recommended.",
    )
    tagline = models.CharField(
        max_length=200,
        blank=True,
        default="We provide website, app, and software solutions to help businesses grow digitally.",
        help_text="Short line shown under the logo in the footer.",
    )
    phone = models.CharField(max_length=30, blank=True, default="+91-1234567890")
    email = models.EmailField(blank=True, default="businessteam@vetriitsystems.com")
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    get_in_touch_text = models.CharField(max_length=40, default="Get in Touch")
    get_in_touch_url = models.CharField(max_length=200, default="/contact/")
    footer_connect_heading = models.CharField(
        max_length=100, default="Let's Connect there"
    )
    copyright_text = models.CharField(
        max_length=200, default="© 2026 Vetri IT Systems. All Rights Reserved."
    )

    contact_button_text = models.CharField(max_length=40, default="Contact Now")
    contact_button_url = models.CharField(max_length=200, default="/contact/")

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError(
                "Only one Site Settings record is allowed. Edit the existing one."
            )
        return super().save(*args, **kwargs)


class NavItem(models.Model):
    """Top navigation menu items. Order + icon fully admin controlled."""

    name = models.CharField(max_length=50)
    url = models.CharField(
        max_length=200, help_text="e.g. /services/ or #services for an anchor link."
    )
    icon_class = models.CharField(
        max_length=60,
        default="ti ti-info-circle",
        help_text="Tabler icon class shown on hover, e.g. 'ti ti-flask'.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Navigation Item"
        verbose_name_plural = "Navigation Items"

    def __str__(self):
        return self.name


class FooterServiceLink(models.Model):
    """'Services' column links in the footer."""

    name = models.CharField(max_length=60)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Footer Service Link"
        verbose_name_plural = "Footer Service Links"

    def __str__(self):
        return self.name


class FooterQuickLink(models.Model):
    """'Quick Links' column links in the footer."""

    name = models.CharField(max_length=60)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Footer Quick Link"
        verbose_name_plural = "Footer Quick Links"

    def __str__(self):
        return self.name
    

# banners
class Banner(models.Model):
    """
    One banner per page. Admin picks which page it belongs to via the
    `page` dropdown, uploads the illustration image, and sets up to
    2 CTA buttons. Reused across About, Services, Solutions, Careers,
    Contact, etc. — each page just pulls its own row.
    """

    PAGE_CHOICES = [
        ("home", "Home"),
        ("about", "About"),
        ("services", "Services"),
        ("our_products", "Our Products"),
        ("solutions", "Solutions"),
        ("careers", "Careers"),
        ("contact", "Contact"),
    ]

    page = models.CharField(
        max_length=20,
        choices=PAGE_CHOICES,
        unique=True,
        help_text="Which page this banner appears on. Only one banner per page.",
    )
    heading = models.CharField(
        max_length=200,
        blank= True,
        help_text="Full heading text, e.g. 'Empowering Businesses with Smart Digital Solutions'.",
    )
    highlight_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Exact word/phrase inside the heading to color purple, e.g. 'Solutions'. Leave blank for no highlight.",
    )
    description = models.TextField(blank=True)
    banner_image = models.ImageField(
        upload_to="banners/",
        blank=True,
        null=True,
        help_text="Illustration/graphic shown on the right side of the banner.",
    )
    cta_1_text = models.CharField(max_length=40, blank=True, default="Explore Services")
    cta_1_url = models.CharField(max_length=200, blank=True, default="/services/")
    cta_2_text = models.CharField(max_length=40, blank=True, default="Contact Us")
    cta_2_url = models.CharField(max_length=200, blank=True, default="/contact/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.get_page_display()
    



# ==========================================================================
# About Page
# ==========================================================================

class AboutIntro(models.Model):
    """Singleton — eyebrow, heading, paragraph, and the one quote card."""

    eyebrow_text = models.CharField(max_length=100, default="About Vetri IT Systems")
    heading = models.CharField(max_length=200, default="Your Strategic Partner in Digital Excellence")
    description = models.TextField(blank=True)
    quote_text = models.CharField(
        max_length=300,
        blank=True,
        help_text="Shown in the quote card between the highlight cards and the intro text.",
    )

    class Meta:
        verbose_name = "About — Intro Section"
        verbose_name_plural = "About — Intro Section"

    def __str__(self):
        return "About Intro"

    def save(self, *args, **kwargs):
        if not self.pk and AboutIntro.objects.exists():
            raise ValidationError("Only one About Intro record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class AboutHighlightCard(models.Model):
    """The 2 purple cards, e.g. 'Vetri Consultancy Service'."""

    image = models.ImageField(upload_to="about/highlight_cards/", blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "About — Highlight Card"
        verbose_name_plural = "About — Highlight Cards"

    def __str__(self):
        return self.title


class AboutChecklistItem(models.Model):
    """The 4 checkmark items, e.g. 'Web & App Development'."""

    text = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "About — Checklist Item"
        verbose_name_plural = "About — Checklist Items"

    def __str__(self):
        return self.text


class AboutStat(models.Model):
    """The stats strip, e.g. '5+ / Years experience since 2021'."""

    number = models.CharField(max_length=20, help_text="e.g. '5+', '500+', '100%', '24/7'")
    label = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "About — Stat"
        verbose_name_plural = "About — Stats"

    def __str__(self):
        return f"{self.number} — {self.label}"


class AboutServiceCard(models.Model):
    """Core Services cards on the About page."""

    image = models.ImageField(upload_to="about/service_cards/", blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "About — Core Service Card"
        verbose_name_plural = "About — Core Service Cards"

    def __str__(self):
        return self.title


class AboutValueSection(models.Model):
    """Singleton — 'How We Deliver Value' heading + side image."""

    heading = models.CharField(max_length=150, default="How We Deliver Value")
    image = models.ImageField(upload_to="about/value_section/", blank=True, null=True)

    class Meta:
        verbose_name = "About — Value Section"
        verbose_name_plural = "About — Value Section"

    def __str__(self):
        return "About Value Section"

    def save(self, *args, **kwargs):
        if not self.pk and AboutValueSection.objects.exists():
            raise ValidationError("Only one Value Section record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class AboutValueStep(models.Model):
    """Numbered steps inside 'How We Deliver Value', e.g. 'Client-Focused Strategy'."""

    step_number = models.PositiveIntegerField(help_text="The number shown in the circle, e.g. 1, 2, 3, 4.")
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "About — Value Step"
        verbose_name_plural = "About — Value Steps"

    def __str__(self):
        return f"{self.step_number}. {self.title}"


class AboutMissionVision(models.Model):
    """The 2 cards: Mission and Vision."""

    image = models.ImageField(upload_to="about/mission_vision/", blank=True, null=True)
    title = models.CharField(max_length=100, help_text="e.g. 'Our Mission' or 'Our Vision'")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "About — Mission / Vision Card"
        verbose_name_plural = "About — Mission / Vision Cards"

    def __str__(self):
        return self.title


class AboutWhySection(models.Model):
    """Singleton — 'Why Work With Us' heading + subheading."""

    heading = models.CharField(max_length=150, default="Why Work With Us")
    subheading = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = "About — Why Section"
        verbose_name_plural = "About — Why Section"

    def __str__(self):
        return "About Why Section"

    def save(self, *args, **kwargs):
        if not self.pk and AboutWhySection.objects.exists():
            raise ValidationError("Only one Why Section record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class AboutWhyCard(models.Model):
    """Cards inside 'Why Work With Us', e.g. '5+ Years of Experience'."""

    image = models.ImageField(upload_to="about/why_cards/", blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "About — Why Card"
        verbose_name_plural = "About — Why Cards"

    def __str__(self):
        return self.title


# ==========================================================================
# Services Page
# ==========================================================================

class ServiceCard(models.Model):
    image = models.ImageField(
        upload_to="services/cards/",
        help_text="Main illustration shown by default (e.g. the 'WEBSITE DEVELOPMENT' graphic).",
    )
    icon = models.ImageField(
        upload_to="services/card_icons/",
        blank=True,
        null=True,
        help_text="Small icon shown in the hover state (e.g. the orange phone icon).",
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    cta_text = models.CharField(max_length=40, default="Explore Service")
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # --- Detail page: banner ---
    detail_banner_heading = models.CharField(max_length=150, blank=True, help_text="e.g. 'Website Services'")
    detail_banner_description = models.TextField(blank=True)
    detail_banner_image = models.ImageField(upload_to="services/detail_banners/", blank=True, null=True)
    detail_banner_cta1_text = models.CharField(max_length=40, default="Get Start")
    detail_banner_cta1_url = models.CharField(max_length=200, default="#")
    detail_banner_cta2_text = models.CharField(max_length=40, default="Contact Us")
    detail_banner_cta2_url = models.CharField(max_length=200, default="/contact/")

    # --- Detail page: small explanation section ---
    detail_explanation_heading = models.CharField(
        max_length=200, blank=True, help_text="e.g. 'Professional Website Development Services'"
    )
    detail_explanation_text = models.TextField(blank=True)

    # --- Detail page: "Our Website Solutions" heading ---
    solutions_heading = models.CharField(max_length=150, blank=True, default="Our Website Solutions")

    # --- Detail page: "What You Get" heading ---
    features_heading = models.CharField(max_length=150, blank=True, default="What You Get")

    class Meta:
        ordering = ["order"]
        verbose_name = "Services — Service Card"
        verbose_name_plural = "Services — Service Cards"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class WorkingProcessStep(models.Model):
    """
    'Our Working Process' steps, connected by a line. Plays as a one-time
    sequential scroll-triggered reveal — step 1 lights up, then the
    connector to step 2, then step 2, and so on.
    """

    icon = models.ImageField(upload_to="services/process_steps/", blank=True, null=True)
    title = models.CharField(max_length=100, help_text="e.g. 'Requirement Analysis'")
    step_number = models.PositiveIntegerField(help_text="Determines the sequence order of the reveal animation.")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Services — Working Process Step"
        verbose_name_plural = "Services — Working Process Steps"

    def __str__(self):
        return f"{self.step_number}. {self.title}"


class IndustryCard(models.Model):
    """'Industries We Serve' cards — icon + title only, no description."""

    icon = models.ImageField(upload_to="services/industries/", blank=True, null=True)
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Services — Industry Card"
        verbose_name_plural = "Services — Industry Cards"

    def __str__(self):
        return self.title
    


# ==========================================================================
# Our Products Page
# ==========================================================================

class ProductCard(models.Model):
    """
    'Our Products' cards. The first card (by order) renders full-width
    with the dashboard screenshot layered beside it. Every other card
    renders in a 2-column grid, screenshot below the text, overflowing
    the card edge. No CTA — icon, title, description, and screenshot only.
    """

    icon = models.ImageField(upload_to="products/icons/")
    title = models.CharField(max_length=150, help_text="e.g. 'VTMS - Vetri Training Management System'")
    description = models.TextField()
    screenshot = models.ImageField(
        upload_to="products/screenshots/",
        help_text="Dashboard/product screenshot shown beside or below the text.",
    )
    url = models.CharField(
        max_length=200,
        default="#",
        help_text="Where clicking the card leads — internal page or external product link.",
    )
    tagline = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short subheading shown on the product detail page, e.g. 'Simplify Billing, Manage Sales, and Grow Your Business'.",
    )
    slug = models.SlugField(max_length=160, unique=True, blank=True)

    order = models.PositiveIntegerField(
        default=0,
        help_text="Card with the lowest order number renders full-width as the featured product.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Products — Product Card"
        verbose_name_plural = "Products — Product Cards"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProductGalleryImage(models.Model):
    """
    Up to 5 (or more) screenshots shown in the horizontally scrollable
    gallery strip on a product's detail page. Linked to one ProductCard.
    """

    product = models.ForeignKey(
        ProductCard, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ImageField(upload_to="products/gallery/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Products — Gallery Image"
        verbose_name_plural = "Products — Gallery Images"

    def __str__(self):
        return f"{self.product.title} — image {self.order}"
    

# ==========================================================================
# Solutions Page
# ==========================================================================

class SolutionCard(models.Model):
    """
    'Smart Digital Solutions for Every Business' cards. Not clickable —
    image, title, description only. On hover: left-edge gradient border
    strip appears and the image mirrors horizontally.
    """

    image = models.ImageField(upload_to="solutions/cards/")
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Solutions — Solution Card"
        verbose_name_plural = "Solutions — Solution Cards"

    def __str__(self):
        return self.title
    
# ==========================================================================
# Careers Page
# ==========================================================================

class CareerHero(models.Model):
    """Singleton — hero section (no shared Banner used on this page)."""

    heading = models.CharField(max_length=200, default="Join the Future of Digital Innovation")
    highlight_text = models.CharField(max_length=100, default="Future")
    description = models.TextField(blank=True)
    cta_text = models.CharField(max_length=40, default="View Open Roles")
    cta_anchor = models.CharField(
        max_length=100,
        default="#open-positions",
        help_text="Anchor link on this same page, e.g. '#open-positions'.",
    )
    image = models.ImageField(upload_to="careers/hero/", blank=True, null=True)

    class Meta:
        verbose_name = "Careers — Hero Section"
        verbose_name_plural = "Careers — Hero Section"

    def __str__(self):
        return "Careers Hero"

    def save(self, *args, **kwargs):
        if not self.pk and CareerHero.objects.exists():
            raise ValidationError("Only one Careers Hero record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class OpenPositionsSection(models.Model):
    """Singleton — heading for the Open Positions section."""

    eyebrow_text = models.CharField(max_length=100, default="Career Opportunities")
    heading = models.CharField(max_length=150, default="Open Positions")

    class Meta:
        verbose_name = "Careers — Open Positions Heading"
        verbose_name_plural = "Careers — Open Positions Heading"

    def __str__(self):
        return "Open Positions Section"

    def save(self, *args, **kwargs):
        if not self.pk and OpenPositionsSection.objects.exists():
            raise ValidationError("Only one record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class JobOpening(models.Model):
    """Individual job rows under Open Positions."""

    icon = models.ImageField(upload_to="careers/job_icons/", blank=True, null=True)
    title = models.CharField(max_length=150, help_text="e.g. 'Senior Product Designer'")
    apply_url = models.URLField(default="https://vetrijobs.com")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Careers — Job Opening"
        verbose_name_plural = "Careers — Job Openings"

    def __str__(self):
        return self.title


class LifeAtVISSection(models.Model):
    """Singleton — heading for the Life at VIS gallery section."""

    heading = models.CharField(max_length=150, default="Life at VIS")
    subheading = models.CharField(max_length=200, default="A glimpse into our world, our people.")

    class Meta:
        verbose_name = "Careers — Life at VIS Heading"
        verbose_name_plural = "Careers — Life at VIS Heading"

    def __str__(self):
        return "Life at VIS Section"

    def save(self, *args, **kwargs):
        if not self.pk and LifeAtVISSection.objects.exists():
            raise ValidationError("Only one record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class LifeAtVISImage(models.Model):
    """
    4-image mosaic gallery. Order 1 = large image (left), orders 2-4 =
    the 3 smaller images (right side grid).
    """

    image = models.ImageField(upload_to="careers/life_at_vis/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Careers — Life at VIS Image"
        verbose_name_plural = "Careers — Life at VIS Images"

    def __str__(self):
        return f"Life at VIS image {self.order}"


class CultureSection(models.Model):
    """Singleton — heading/description for Our Culture."""

    heading = models.CharField(max_length=150, default="Our Culture")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Careers — Culture Heading"
        verbose_name_plural = "Careers — Culture Heading"

    def __str__(self):
        return "Culture Section"

    def save(self, *args, **kwargs):
        if not self.pk and CultureSection.objects.exists():
            raise ValidationError("Only one record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class CultureCard(models.Model):
    """Cards inside Our Culture, e.g. 'Remote First'."""

    icon = models.ImageField(upload_to="careers/culture_icons/", blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Careers — Culture Card"
        verbose_name_plural = "Careers — Culture Cards"

    def __str__(self):
        return self.title


class BenefitsSection(models.Model):
    """Singleton — heading/subheading for Our Benefits."""

    heading = models.CharField(max_length=150, default="Our Benefits")
    subheading = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = "Careers — Benefits Heading"
        verbose_name_plural = "Careers — Benefits Heading"

    def __str__(self):
        return "Benefits Section"

    def save(self, *args, **kwargs):
        if not self.pk and BenefitsSection.objects.exists():
            raise ValidationError("Only one record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class BenefitCard(models.Model):
    """Cards inside Our Benefits, e.g. 'Premium Healthcare'."""

    icon = models.ImageField(upload_to="careers/benefit_icons/", blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Careers — Benefit Card"
        verbose_name_plural = "Careers — Benefit Cards"

    def __str__(self):
        return self.title


# ==========================================================================
# Shared "Let's Build Something" CTA — appears on every page, above footer
# ==========================================================================

class BuildSomethingCTA(models.Model):
    """Singleton. Shown right above the footer on every page."""

    heading = models.CharField(max_length=200, default="Let's Build Something Amazing Together")
    description = models.TextField(
        blank=True,
        default="Ready to take your digital presence to the next level? Our team is standing by to help you scale.",
    )
    primary_button_text = models.CharField(max_length=40, default="Start Your Project")
    secondary_button_text = models.CharField(max_length=40, default="Enquiry")
    button_url = models.CharField(
        max_length=200,
        default="/contact/",
        help_text="Both buttons link here.",
    )

    class Meta:
        verbose_name = "Build Something CTA (shared)"
        verbose_name_plural = "Build Something CTA (shared)"

    def __str__(self):
        return "Build Something CTA"

    def save(self, *args, **kwargs):
        if not self.pk and BuildSomethingCTA.objects.exists():
            raise ValidationError("Only one record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)




# ==========================================================================
# Contact Page
# ==========================================================================

class ContactPageInfo(models.Model):
    """
    Singleton. Holds the phone number shown under 'Call Us', the company
    email that receives 'Send Message' form submissions, and the Google
    Maps embed URL.
    """

    call_us_number = models.CharField(max_length=30, default="+91-1234567890")
    company_email = models.EmailField(
        help_text="Where 'Send Message' form submissions are delivered."
    )
    map_embed_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Google Maps: Share > Embed a map > copy the src URL from the iframe code.",
    )

    class Meta:
        verbose_name = "Contact — Page Info"
        verbose_name_plural = "Contact — Page Info"

    def __str__(self):
        return "Contact Page Info"

    def save(self, *args, **kwargs):
        if not self.pk and ContactPageInfo.objects.exists():
            raise ValidationError("Only one record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class ContactLocation(models.Model):
    """'Visit Us' repeatable branch addresses."""

    branch_name = models.CharField(
        max_length=150, help_text="e.g. 'Surandai - Shanthi Complex - Branch 1'"
    )
    address = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Contact — Location"
        verbose_name_plural = "Contact — Locations"

    def __str__(self):
        return self.branch_name


class FAQ(models.Model):
    """Admin-controlled FAQs. Section scrolls if more than 4 are active."""

    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Contact — FAQ"
        verbose_name_plural = "Contact — FAQs"

    def __str__(self):
        return self.question


class ContactSubmission(models.Model):
    """
    Stores every 'Send Message' form submission, in addition to emailing
    the company. Lets you review leads in admin even if an email bounces.
    """

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Contact — Form Submission"
        verbose_name_plural = "Contact — Form Submissions"

    def __str__(self):
        return f"{self.name} — {self.submitted_at:%Y-%m-%d %H:%M}"
    


# ==========================================================================
# Home Page — Hero
# ==========================================================================

class HomeHero(models.Model):
    """
    Singleton. Custom homepage banner with two character illustrations —
    distinct from the shared Banner model used on other pages.
    """

    heading = models.CharField(
        max_length=200,
        default="We Build Websites, Apps &Software That Grow Your Business",
    )
    highlight_text = models.CharField(
        max_length=100,
        default="Grow Your Business",
        help_text="Portion of the heading colored purple.",
    )
    description = models.TextField(blank=True)
    cta_1_text = models.CharField(max_length=40, default="Get Start")
    cta_1_url = models.CharField(max_length=200, default="#")
    cta_2_text = models.CharField(max_length=40, default="View Our Services")
    cta_2_url = models.CharField(max_length=200, default="/services/")
    background_image = models.ImageField(
        upload_to="home/hero/",
        blank=True,
        null=True,
        help_text="Abstract gradient/shapes background layer, sits behind both characters.",
    )
    sitting_man_image = models.ImageField(
        upload_to="home/hero/",
        blank=True,
        null=True,
        help_text="Static character, no animation.",
    )
    standing_man_image = models.ImageField(
        upload_to="home/hero/",
        blank=True,
        null=True,
        help_text="Character that continuously floats up and down.",
    )

    class Meta:
        verbose_name = "Home — Hero Section"
        verbose_name_plural = "Home — Hero Section"

    def __str__(self):
        return "Home Hero"

    def save(self, *args, **kwargs):
        if not self.pk and HomeHero.objects.exists():
            raise ValidationError("Only one Home Hero record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)



# ==========================================================================
# Home Page — About Section
# ==========================================================================

class HomeAboutSection(models.Model):
    """Singleton — 'About Vetri IT System' section on the homepage."""

    heading = models.CharField(max_length=150, default="About Vetri IT System")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="home/about/", blank=True, null=True)
    cta_text = models.CharField(max_length=40, default="Learn More")
    cta_url = models.CharField(max_length=200, default="/about/")

    class Meta:
        verbose_name = "Home — About Section"
        verbose_name_plural = "Home — About Section"

    def __str__(self):
        return "Home About Section"

    def save(self, *args, **kwargs):
        if not self.pk and HomeAboutSection.objects.exists():
            raise ValidationError("Only one record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class HomeAboutChecklistItem(models.Model):
    """Repeatable checklist items, e.g. 'Complete Digital Solutions'."""

    text = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Home — About Checklist Item"
        verbose_name_plural = "Home — About Checklist Items"

    def __str__(self):
        return self.text


# ==========================================================================
# Home Page — Working Process (rocket path)
# ==========================================================================
class HomeProcessSection(models.Model):
    """Singleton — just the heading above the rocket-path artwork."""

    heading = models.CharField(max_length=150, default="Our Working Process")

    class Meta:
        verbose_name = "Home — Process Section"
        verbose_name_plural = "Home — Process Section"

    def __str__(self):
        return "Home Process Section"

    def save(self, *args, **kwargs):
        if not self.pk and HomeProcessSection.objects.exists():
            raise ValidationError("Only one record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class HomeProcessFrame(models.Model):
    """
    One frame of the rocket-path sequence (e.g. frame 1 = empty path,
    frame 2 = step 1 revealed, ... frame 7 = all steps revealed).
    Frames crossfade in order, looping forever.
    """

    image = models.ImageField(upload_to="home/process_frames/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Home — Process Frame"
        verbose_name_plural = "Home — Process Frames"

    def __str__(self):
        return f"Process frame {self.order}"


# ==========================================================================
# Home Page — Exclusive Services
# ==========================================================================

class HomeServiceCard(models.Model):
    """
    'We Provide Exclusive Service for your Business' cards. Same design
    as SolutionCard (Solutions page) — image, title, description, with
    the left gradient border + image mirror flip on hover.
    """

    image = models.ImageField(upload_to="home/service_cards/")
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Home — Exclusive Service Card"
        verbose_name_plural = "Home — Exclusive Service Cards"

    def __str__(self):
        return self.title


# ==========================================================================
# Home Page — Why Work With Us
# ==========================================================================

class HomeWhySection(models.Model):
    """Singleton — heading/subheading for the homepage's own 'Why Work With Us'."""

    heading = models.CharField(max_length=150, default="Why Work With Us")
    subheading = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = "Home — Why Section"
        verbose_name_plural = "Home — Why Section"

    def __str__(self):
        return "Home Why Section"

    def save(self, *args, **kwargs):
        if not self.pk and HomeWhySection.objects.exists():
            raise ValidationError("Only one record is allowed. Edit the existing one.")
        return super().save(*args, **kwargs)


class HomeWhyCard(models.Model):
    """Cards inside the homepage's 'Why Work With Us' section."""

    icon = models.ImageField(upload_to="home/why_icons/", blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Home — Why Card"
        verbose_name_plural = "Home — Why Cards"

    def __str__(self):
        return self.title


class ServiceSolutionCard(models.Model):
    """
    Default state: default_image + title only.
    Hover state: orange icon square, title, description, price flag,
    and a repeatable checklist (2-column).
    """

    service = models.ForeignKey(ServiceCard, on_delete=models.CASCADE, related_name="solution_cards")
    default_image = models.ImageField(upload_to="services/solution_cards/default/")
    title = models.CharField(max_length=150)

    # --- Hover state fields ---
    hover_icon = models.ImageField(
        upload_to="services/solution_cards/hover_icons/",
        blank=True,
        null=True,
        help_text="Small icon shown inside the orange rotating square on hover.",
    )
    hover_description = models.CharField(max_length=250, blank=True)
    price_text = models.CharField(
        max_length=40,
        blank=True,
        help_text="e.g. '10,000' — shown in the 'Starting From' flag.",
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Services — Solution Card"
        verbose_name_plural = "Services — Solution Cards"

    def __str__(self):
        return f"{self.service.title} — {self.title}"


class ServiceSolutionChecklistItem(models.Model):
    """Repeatable checklist items shown in the hover state, 2-column layout."""

    solution_card = models.ForeignKey(
        ServiceSolutionCard, on_delete=models.CASCADE, related_name="checklist_items"
    )
    text = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Services — Solution Checklist Item"
        verbose_name_plural = "Services — Solution Checklist Items"

    def __str__(self):
        return self.text


class ServiceFeature(models.Model):
    """'What You Get' pill list items on a service detail page."""

    service = models.ForeignKey(ServiceCard, on_delete=models.CASCADE, related_name="features")
    icon = models.ImageField(upload_to="services/features/", blank=True, null=True)
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Services — Feature"
        verbose_name_plural = "Services — Features"

    def __str__(self):
        return f"{self.service.title} — {self.title}"