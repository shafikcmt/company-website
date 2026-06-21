from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


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
    "COLORS": {
        "primary": {
            "50": "255 251 235",
            "100": "254 243 199",
            "200": "253 230 138",
            "300": "252 211 77",
            "400": "251 191 36",
            "500": "245 158 11",
            "600": "217 119 6",
            "700": "180 83 9",
            "800": "146 64 14",
            "900": "120 53 15",
            "950": "69 26 3",
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
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Global Settings"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Site Settings"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:hapl_sitesettings_changelist"),
                    },
                    {
                        "title": _("Navbar Settings"),
                        "icon": "menu",
                        "link": reverse_lazy("admin:hapl_navbarsettings_changelist"),
                    },
                    {
                        "title": _("Mail Settings"),
                        "icon": "mail",
                        "link": reverse_lazy("admin:hapl_mailsettings_changelist"),
                    },
                ],
            },
            {
                "title": _("Home Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Hero Banner"),
                        "icon": "image",
                        "link": reverse_lazy("admin:hapl_homeherosection_changelist"),
                    },
                    {
                        "title": _("Introduction"),
                        "icon": "info",
                        "link": reverse_lazy(
                            "admin:hapl_homeintroductionsection_changelist"
                        ),
                    },
                    {
                        "title": _("Services"),
                        "icon": "build",
                        "link": reverse_lazy(
                            "admin:hapl_homeservicessection_changelist"
                        ),
                    },
                    {
                        "title": _("Stats"),
                        "icon": "bar_chart",
                        "link": reverse_lazy("admin:hapl_homestatssection_changelist"),
                    },
                ],
            },
            {
                "title": _("About Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("About Section"),
                        "icon": "corporate_fare",
                        "link": reverse_lazy("admin:hapl_aboutsection_changelist"),
                    },
                    {
                        "title": _("Team"),
                        "icon": "group",
                        "link": reverse_lazy("admin:hapl_teamsection_changelist"),
                    },
                    {
                        "title": _("FAQ"),
                        "icon": "help",
                        "link": reverse_lazy("admin:hapl_faqsection_changelist"),
                    },
                ],
            },
            {
                "title": _("Customers Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Customers"),
                        "icon": "handshake",
                        "link": reverse_lazy("admin:hapl_customerssection_changelist"),
                    },
                    {
                        "title": _("Testimonials"),
                        "icon": "format_quote",
                        "link": reverse_lazy(
                            "admin:hapl_testimonialssection_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _("Contact Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Contact Section"),
                        "icon": "contact_page",
                        "link": reverse_lazy("admin:hapl_contactsection_changelist"),
                    },
                    {
                        "title": _("Contact Data"),
                        "icon": "location_on",
                        "link": reverse_lazy("admin:hapl_contactdata_changelist"),
                    },
                ],
            },
            {
                "title": _("Activities Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Activities"),
                        "icon": "volunteer_activism",
                        "link": reverse_lazy("admin:hapl_activitiessection_changelist"),
                    },
                ],
            },
            {
                "title": _("Career Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Career"),
                        "icon": "work",
                        "link": reverse_lazy("admin:hapl_careersection_changelist"),
                    },
                    {
                        "title": _("Applications"),
                        "icon": "description",
                        "link": reverse_lazy("admin:hapl_jobapplication_changelist"),
                    },
                ],
            },
            {
                "title": _("Products Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:hapl_productspage_changelist"),
                    },
                ],
            },
            {
                "title": _("Compliance Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Compliance"),
                        "icon": "verified",
                        "link": reverse_lazy("admin:hapl_compliancepage_changelist"),
                    },
                ],
            },
            {
                "title": _("Sustainability Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Sustainability"),
                        "icon": "eco",
                        "link": reverse_lazy(
                            "admin:hapl_sustainabilitypage_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _("Gallery Page"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Gallery"),
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:hapl_gallerypage_changelist"),
                    },
                    {
                        "title": _("Gallery Sections"),
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:hapl_gallerysection_changelist"),
                    },
                    {
                        "title": _("Gallery Images"),
                        "icon": "image",
                        "link": reverse_lazy("admin:hapl_galleryimage_changelist"),
                    },
                    {
                        "title": _("Gallery Videos"),
                        "icon": "play_circle",
                        "link": reverse_lazy("admin:hapl_galleryvideo_changelist"),
                    },
                ],
            },
            {
                "title": _("System"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": _("Audit Log"),
                        "icon": "history",
                        "link": reverse_lazy("admin:auditlog_logentry_changelist"),
                    },
                ],
            },
        ],
    },
    "DASHBOARD_CALLBACK": "hapl.dashboard.dashboard_callback",
}
