from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def _view_permission(url_name):
    """'admin:hapl_product_changelist' -> callback checking hapl.view_product,
    so each editor only sees the sections their roles allow."""
    app_model = url_name.split(":", 1)[1].rsplit("_", 1)[0]
    app_label, model = app_model.split("_", 1)
    perm = f"{app_label}.view_{model}"
    return lambda request: request.user.has_perm(perm)


def _link(title, icon, url_name):
    item = {"title": title, "icon": icon, "link": reverse_lazy(url_name)}
    if url_name.endswith("_changelist"):
        item["permission"] = _view_permission(url_name)
    return item


def _group(title, *items):
    return {"title": title, "separator": True, "collapsible": True, "items": list(items)}


UNFOLD_CONFIG = {
    "SITE_TITLE": "HAPL Admin",
    "SITE_HEADER": "Humana Apparels",
    "SITE_SUBHEADER": "Content Management System",
    "SITE_URL": "/",
    # No SITE_ICON: an image logo here overflowed and broke the sidebar layout.
    # Branding is text (SITE_HEADER) + a Material Symbol instead.
    "SITE_SYMBOL": "checkroom",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "BORDER_RADIUS": "8px",
    # Brand navy (#093E61 = 600) as the admin primary colour.
    "COLORS": {
        "primary": {
            "50": "#EEF5FA",
            "100": "#D6E6F1",
            "200": "#ADCDE4",
            "300": "#78A6C9",
            "400": "#3A76A3",
            "500": "#0E4A75",
            "600": "#093E61",
            "700": "#07344F",
            "800": "#06293F",
            "900": "#041F30",
            "950": "#02121D",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Dashboard"),
                "separator": False,
                "collapsible": True,
                "items": [_link(_("Dashboard"), "dashboard", "admin:index")],
            },
            _group(
                _("Site Settings"),
                _link(_("Site settings"), "settings", "admin:hapl_sitesettings_changelist"),
                _link(_("Navigation"), "menu", "admin:hapl_navbarsettings_changelist"),
                _link(_("Social links"), "share", "admin:hapl_social_changelist"),
                _link(_("Mail settings"), "mail", "admin:hapl_mailsettings_changelist"),
            ),
            _group(
                _("Home"),
                _link(_("Hero"), "view_carousel", "admin:hapl_homeherosection_changelist"),
                _link(_("Hero slides"), "photo_library", "admin:hapl_homecarouselslide_changelist"),
                _link(_("Introduction"), "info", "admin:hapl_homeintroductionsection_changelist"),
                _link(_("Services"), "design_services", "admin:hapl_homeservicessection_changelist"),
                _link(_("Stats"), "monitoring", "admin:hapl_homestatssection_changelist"),
            ),
            _group(
                _("About"),
                _link(_("About page"), "corporate_fare", "admin:hapl_aboutsection_changelist"),
                _link(_("Core values"), "diamond", "admin:hapl_whyussection_changelist"),
                _link(_("Team"), "groups", "admin:hapl_teamsection_changelist"),
                _link(_("FAQ"), "help", "admin:hapl_faqsection_changelist"),
            ),
            _group(
                _("Products"),
                _link(_("Products page"), "storefront", "admin:hapl_productspage_changelist"),
                _link(_("Categories"), "category", "admin:hapl_productcategory_changelist"),
                _link(_("Products"), "checkroom", "admin:hapl_product_changelist"),
            ),
            _group(
                _("Customers"),
                _link(_("Customers page"), "handshake", "admin:hapl_customerssection_changelist"),
                _link(_("Customers"), "business", "admin:hapl_customer_changelist"),
                _link(_("Testimonials"), "format_quote", "admin:hapl_testimonialssection_changelist"),
            ),
            _group(
                _("Compliance"),
                _link(_("Compliance page"), "verified", "admin:hapl_compliancepage_changelist"),
                _link(_("Audit status"), "fact_check", "admin:hapl_auditstatus_changelist"),
                _link(_("Certificates"), "workspace_premium", "admin:hapl_compliancecertificate_changelist"),
            ),
            _group(
                _("Sustainability"),
                _link(_("Sustainability page"), "eco", "admin:hapl_sustainabilitypage_changelist"),
            ),
            _group(
                _("Gallery"),
                _link(_("Gallery page"), "photo_library", "admin:hapl_gallerypage_changelist"),
                _link(_("Sections"), "folder", "admin:hapl_gallerysection_changelist"),
                _link(_("Images"), "image", "admin:hapl_galleryimage_changelist"),
                _link(_("Videos"), "play_circle", "admin:hapl_galleryvideo_changelist"),
            ),
            _group(
                _("News & Activities"),
                _link(_("Activities page"), "newspaper", "admin:hapl_activitiessection_changelist"),
                _link(_("Activities"), "volunteer_activism", "admin:hapl_activity_changelist"),
            ),
            _group(
                _("Career"),
                _link(_("Career page"), "work", "admin:hapl_careersection_changelist"),
                _link(_("Positions"), "badge", "admin:hapl_careerposition_changelist"),
                _link(_("Applications"), "description", "admin:hapl_jobapplication_changelist"),
            ),
            _group(
                _("Contact"),
                _link(_("Contact page"), "contact_page", "admin:hapl_contactsection_changelist"),
                _link(_("Office & map"), "location_on", "admin:hapl_contactdata_changelist"),
                _link(_("Contact groups"), "contacts", "admin:hapl_contactgroup_changelist"),
            ),
            _group(
                _("System"),
                _link(_("Users"), "manage_accounts", "admin:users_user_changelist"),
                _link(_("Roles"), "admin_panel_settings", "admin:users_role_changelist"),
                _link(_("Audit log"), "history", "admin:auditlog_logentry_changelist"),
            ),
        ],
    },
    "DASHBOARD_CALLBACK": "hapl.dashboard.dashboard_callback",
}
