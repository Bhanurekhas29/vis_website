from .models import (
    BuildSomethingCTA,
    FooterQuickLink,
    FooterServiceLink,
    NavItem,
    SiteSettings,
)

def site_globals(request):
    return {
        "site_settings": SiteSettings.objects.first(),
        "nav_items": NavItem.objects.filter(is_active=True).order_by("order"),
        "footer_service_links": FooterServiceLink.objects.filter(
            is_active=True
        ).order_by("order"),
        "footer_quick_links": FooterQuickLink.objects.filter(
            is_active=True
        ).order_by("order"),
        "build_cta": BuildSomethingCTA.objects.first(),
    }