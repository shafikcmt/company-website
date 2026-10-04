"""Global template context shared across every page on the public site."""

import logging

from django.urls import reverse

from hapl.models import SiteSettings, NavbarSettings, Social

logger = logging.getLogger(__name__)


# The public pages are fixed by hapl/urls.py, so the menu is declared here
# (url name, label, NavbarSettings flag) and only its visibility is editable
# from the admin via NavbarSettings. A free-form NavItem model would let
# editors link to pages that do not exist and would duplicate NavbarSettings.
NAV_ITEMS = (
    ("home", "Home", "show_home"),
    ("about", "About", "show_about"),
    ("products", "Products", "show_products"),
    ("customers", "Customers", "show_customers"),
    ("complience", "Compliance", "show_compliance"),
    ("sustainability", "Sustainability", "show_sustainability"),
    ("gallery", "Gallery", "show_gallery"),
    ("activities", "Activities", "show_activities"),
    ("career", "Career", "show_career"),
    ("contact", "Contact", "show_contact"),
)

# Sub-pages that should highlight their parent menu entry.
ACTIVE_ALIASES = {"career_apply": "career"}


def site_context(request):
    """Inject SiteSettings, NavbarSettings, the nav menu and social links.

    Wrapped defensively so a missing table (e.g. before migrations run) or an
    empty database never raises a 500 — templates fall back to defaults.
    """
    site = navbar = None
    socials = []
    try:
        site = SiteSettings.objects.first()
        navbar = NavbarSettings.objects.first()
        socials = list(Social.objects.order_by("order", "id"))
    except Exception:  # pragma: no cover - DB not ready
        logger.debug("Site context unavailable", exc_info=True)

    match = getattr(request, "resolver_match", None)
    current = match.url_name if match else None
    current = ACTIVE_ALIASES.get(current, current)

    nav_items = []
    for url_name, label, flag in NAV_ITEMS:
        if navbar is not None and not getattr(navbar, flag, True):
            continue
        nav_items.append(
            {
                "url_name": url_name,
                "label": label,
                "url": reverse(url_name),
                "active": url_name == current,
            }
        )

    return {
        # Blank instance when no row exists, so templates can chain defaults.
        "site": site if site is not None else SiteSettings(),
        "navbar": navbar,
        "nav_items": nav_items,
        # Contact is rendered as the header CTA, not as a plain link.
        "nav_links": [item for item in nav_items if item["url_name"] != "contact"],
        "contact_visible": any(i["url_name"] == "contact" for i in nav_items),
        "footer_socials": socials,
    }
