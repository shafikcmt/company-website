"""Ready-made content roles for the admin.

Each role grants view/add/change/delete on the models behind one part of the
website, so an editor can be limited to e.g. the Gallery. Roles are created
after `migrate` (see users/apps.py) and can be edited in the admin; run
`python manage.py sync_roles` to reset them to these defaults.
"""

from django.contrib.auth.models import Permission
from django.db.models import Q

ACTIONS = ("view", "add", "change", "delete")

SECTION_MODELS = {
    "Site settings": ("sitesettings", "navbarsettings", "social"),
    "Home page": (
        "homeherosection", "homecarouselslide", "homeintroductionsection",
        "homeintroductionfeature", "homeservicessection", "service",
        "homestatssection", "companystats",
    ),
    "About page": (
        "aboutsection", "whyussection", "whyusfeature", "teamsection",
        "teammember", "faqsection", "faq",
    ),
    "Products": (
        "productspage", "productcarouselslide", "productsection",
        "productcategory", "product",
    ),
    "Customers": ("customerssection", "customer", "testimonialssection", "testimonial"),
    "Compliance": ("compliancepage", "compliancesection", "compliancecertificate", "auditstatus"),
    "Sustainability": ("sustainabilitypage", "sustainabilitysection", "sustainabilitycertificate"),
    "Gallery": ("gallerypage", "gallerysection", "galleryimage", "galleryvideo"),
    "News & Activities": ("activitiessection", "activity"),
    "Career & HR": ("careersection", "careerposition", "jobapplication"),
    "Contact page": (
        "contactsection", "contactdata", "contactphone", "contactemail",
        "contactgroup", "contactmember",
    ),
}

# Every page except site-wide settings, mail and user management.
ALL_PAGES = "Content editor (all pages)"
ROLE_NAMES = tuple(SECTION_MODELS) + (ALL_PAGES,)


def role_models(name):
    if name == ALL_PAGES:
        return tuple(
            model for section, models in SECTION_MODELS.items()
            if section != "Site settings" for model in models
        )
    return SECTION_MODELS[name]


def role_permissions(name):
    models = role_models(name)
    codenames = [f"{action}_{model}" for model in models for action in ACTIONS]
    return Permission.objects.filter(
        Q(content_type__app_label="hapl") & Q(content_type__model__in=models) & Q(codename__in=codenames)
    )


def sync_roles(reset=False):
    """Create missing roles with their default permissions. With reset=True
    existing roles are set back to the defaults too. Returns roles touched."""
    from users.models import Role

    touched = []
    for name in ROLE_NAMES:
        role, created = Role.objects.get_or_create(name=name)
        if created or reset:
            role.permissions.set(role_permissions(name))
            touched.append(role)
    return touched
