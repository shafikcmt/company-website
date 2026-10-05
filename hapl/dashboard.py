from django.urls import reverse

from hapl.models import (
    Activity,
    CareerPosition,
    Customer,
    GalleryImage,
    JobApplication,
    Product,
    TeamMember,
    Testimonial,
)


def _url(name):
    return reverse(f"admin:hapl_{name}_changelist")


def dashboard_callback(request, context):
    """Stat cards, shortcuts and recent items for the admin dashboard."""
    new_applications = JobApplication.objects.filter(status="new").count()
    context.update(
        {
            "dashboard_stats": [
                {"label": "Activities", "value": Activity.objects.count(), "icon": "volunteer_activism", "url": _url("activity")},
                {"label": "Open positions", "value": CareerPosition.objects.filter(status="active").count(), "icon": "work", "url": _url("careerposition")},
                {"label": "New applications", "value": new_applications, "icon": "inbox", "url": _url("jobapplication") + "?status__exact=new", "highlight": new_applications > 0},
                {"label": "Clients", "value": Customer.objects.count(), "icon": "handshake", "url": _url("customer")},
                {"label": "Products", "value": Product.objects.count(), "icon": "checkroom", "url": _url("product")},
                {"label": "Gallery images", "value": GalleryImage.objects.count(), "icon": "photo_library", "url": _url("galleryimage")},
                {"label": "Team members", "value": TeamMember.objects.count(), "icon": "group", "url": _url("teammember")},
                {"label": "Testimonials", "value": Testimonial.objects.count(), "icon": "format_quote", "url": _url("testimonial")},
            ],
            "quick_actions": [
                {"label": "Home hero", "hint": "Slides & headline", "icon": "view_carousel", "url": _url("homeherosection")},
                {"label": "New activity", "hint": "Publish news", "icon": "add_circle", "url": reverse("admin:hapl_activity_add")},
                {"label": "New position", "hint": "Post a job", "icon": "person_add", "url": reverse("admin:hapl_careerposition_add")},
                {"label": "Products", "hint": "Catalogue", "icon": "inventory_2", "url": _url("productspage")},
                {"label": "Gallery", "hint": "Photos & videos", "icon": "photo_library", "url": _url("gallerypage")},
                {"label": "Site settings", "hint": "Logo, footer, SEO", "icon": "settings", "url": _url("sitesettings")},
            ],
            "recent_activities": Activity.objects.order_by("-activity_date")[:5],
            "activities_url": _url("activity"),
            "active_positions": CareerPosition.objects.filter(status="active").order_by("-posted_at")[:5],
            "positions_url": _url("careerposition"),
            "recent_applications": JobApplication.objects.select_related("position").order_by("-created_at")[:5],
            "applications_url": _url("jobapplication"),
        }
    )
    return context
