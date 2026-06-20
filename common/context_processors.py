"""Global template context shared across every page on the public site."""

from hapl.models import SiteSettings, NavbarSettings


def global_settings(request):
    """Inject the singleton SiteSettings / NavbarSettings into all templates.

    Wrapped defensively so a missing table (e.g. before migrations run) or an
    empty database never raises a 500 — templates simply fall back to defaults.
    """
    site = None
    navbar = None
    try:
        site = SiteSettings.objects.first()
        navbar = NavbarSettings.objects.first()
    except Exception:
        pass

    return {
        "site": site,
        "navbar": navbar,
    }
