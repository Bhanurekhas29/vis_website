from django.contrib import admin

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
    BuildSomethingCTA,
    CareerHero,
    ContactLocation,
    ContactPageInfo,
    ContactSubmission,
    CultureCard,
    CultureSection,
    FAQ,
    FooterQuickLink,
    FooterServiceLink,
    HomeAboutChecklistItem,
    HomeAboutSection,
    HomeHero,
    HomeProcessFrame,
    HomeProcessSection,
    HomeServiceCard,
    HomeWhyCard,
    HomeWhySection,
    IndustryCard,
    JobOpening,
    LifeAtVISImage,
    LifeAtVISSection,
    NavItem,
    OpenPositionsSection,
    ProductCard,
    ProductGalleryImage,
    ServiceCard,
    ServiceFeature,
    ServiceSolutionCard,
    ServiceSolutionChecklistItem,
    SiteSettings,
    SolutionCard,
    WorkingProcessStep,
)


# ==========================================================================
# Core / Global
# ==========================================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_title", "phone", "email")
    search_fields = ("site_title", "email", "phone")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "icon_class", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "url")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(FooterServiceLink)
class FooterServiceLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "url")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(FooterQuickLink)
class FooterQuickLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "url")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("get_page_display", "heading", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("heading", "description")
    list_filter = ("page", "is_active")
    ordering = ("order",)

    @admin.display(description="Page")
    def get_page_display(self, obj):
        return obj.get_page_display()


@admin.register(BuildSomethingCTA)
class BuildSomethingCTAAdmin(admin.ModelAdmin):
    list_display = ("heading",)

    def has_add_permission(self, request):
        return not BuildSomethingCTA.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ==========================================================================
# About Page
# ==========================================================================

@admin.register(AboutIntro)
class AboutIntroAdmin(admin.ModelAdmin):
    list_display = ("heading", "eyebrow_text")
    search_fields = ("heading", "eyebrow_text", "description", "quote_text")

    def has_add_permission(self, request):
        return not AboutIntro.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutHighlightCard)
class AboutHighlightCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(AboutChecklistItem)
class AboutChecklistItemAdmin(admin.ModelAdmin):
    list_display = ("text", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("text",)
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(AboutStat)
class AboutStatAdmin(admin.ModelAdmin):
    list_display = ("number", "label", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("number", "label")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(AboutServiceCard)
class AboutServiceCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(AboutValueSection)
class AboutValueSectionAdmin(admin.ModelAdmin):
    list_display = ("heading",)
    search_fields = ("heading",)

    def has_add_permission(self, request):
        return not AboutValueSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutValueStep)
class AboutValueStepAdmin(admin.ModelAdmin):
    list_display = ("step_number", "title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(AboutMissionVision)
class AboutMissionVisionAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(AboutWhySection)
class AboutWhySectionAdmin(admin.ModelAdmin):
    list_display = ("heading", "subheading")
    search_fields = ("heading", "subheading")

    def has_add_permission(self, request):
        return not AboutWhySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutWhyCard)
class AboutWhyCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)


# ==========================================================================
# Services Page
# ==========================================================================

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ("icon", "title", "order", "is_active")


@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ServiceFeatureInline]


class ServiceSolutionChecklistItemInline(admin.TabularInline):
    model = ServiceSolutionChecklistItem
    extra = 1
    fields = ("text", "order", "is_active")


@admin.register(ServiceSolutionCard)
class ServiceSolutionCardAdmin(admin.ModelAdmin):
    list_display = ("title", "service", "price_text", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "hover_description")
    list_filter = ("service", "is_active")
    ordering = ("order",)
    inlines = [ServiceSolutionChecklistItemInline]


@admin.register(WorkingProcessStep)
class WorkingProcessStepAdmin(admin.ModelAdmin):
    list_display = ("step_number", "title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(IndustryCard)
class IndustryCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)
    ordering = ("order",)


# ==========================================================================
# Our Products Page
# ==========================================================================

class ProductGalleryImageInline(admin.TabularInline):
    model = ProductGalleryImage
    extra = 1
    fields = ("image", "order", "is_active")


@admin.register(ProductCard)
class ProductCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductGalleryImageInline]


# ==========================================================================
# Solutions Page
# ==========================================================================

@admin.register(SolutionCard)
class SolutionCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)


# ==========================================================================
# Careers Page
# ==========================================================================

@admin.register(CareerHero)
class CareerHeroAdmin(admin.ModelAdmin):
    list_display = ("heading",)

    def has_add_permission(self, request):
        return not CareerHero.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OpenPositionsSection)
class OpenPositionsSectionAdmin(admin.ModelAdmin):
    list_display = ("heading", "eyebrow_text")

    def has_add_permission(self, request):
        return not OpenPositionsSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ("title", "apply_url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(LifeAtVISSection)
class LifeAtVISSectionAdmin(admin.ModelAdmin):
    list_display = ("heading", "subheading")

    def has_add_permission(self, request):
        return not LifeAtVISSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LifeAtVISImage)
class LifeAtVISImageAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "is_active")
    list_display_links = ("id",)
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(CultureSection)
class CultureSectionAdmin(admin.ModelAdmin):
    list_display = ("heading",)

    def has_add_permission(self, request):
        return not CultureSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CultureCard)
class CultureCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(BenefitsSection)
class BenefitsSectionAdmin(admin.ModelAdmin):
    list_display = ("heading", "subheading")

    def has_add_permission(self, request):
        return not BenefitsSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BenefitCard)
class BenefitCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)


# ==========================================================================
# Contact Page
# ==========================================================================

@admin.register(ContactPageInfo)
class ContactPageInfoAdmin(admin.ModelAdmin):
    list_display = ("call_us_number", "company_email")

    def has_add_permission(self, request):
        return not ContactPageInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactLocation)
class ContactLocationAdmin(admin.ModelAdmin):
    list_display = ("branch_name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("branch_name", "address")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("question", "answer")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "submitted_at")
    search_fields = ("name", "email", "phone", "message")
    list_filter = ("submitted_at",)
    ordering = ("-submitted_at",)
    readonly_fields = ("name", "email", "phone", "message", "submitted_at")

    def has_add_permission(self, request):
        return False


# ==========================================================================
# Home Page
# ==========================================================================

@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    list_display = ("heading",)

    def has_add_permission(self, request):
        return not HomeHero.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomeAboutSection)
class HomeAboutSectionAdmin(admin.ModelAdmin):
    list_display = ("heading",)

    def has_add_permission(self, request):
        return not HomeAboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomeAboutChecklistItem)
class HomeAboutChecklistItemAdmin(admin.ModelAdmin):
    list_display = ("text", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("text",)
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(HomeProcessSection)
class HomeProcessSectionAdmin(admin.ModelAdmin):
    list_display = ("heading",)

    def has_add_permission(self, request):
        return not HomeProcessSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomeProcessFrame)
class HomeProcessFrameAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "is_active")
    list_display_links = ("id",)
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(HomeServiceCard)
class HomeServiceCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)


@admin.register(HomeWhySection)
class HomeWhySectionAdmin(admin.ModelAdmin):
    list_display = ("heading", "subheading")

    def has_add_permission(self, request):
        return not HomeWhySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomeWhyCard)
class HomeWhyCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("order",)