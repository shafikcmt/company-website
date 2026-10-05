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
    """Stat cards, shortcuts and recent items for the admin dashboard, limited
    to what the signed-in user's roles allow."""
    user = request.user

    def can(action, model):
        return user.has_perm(f"hapl.{action}_{model}")

    stats = [
        ("activity", "Activities", "volunteer_activism", lambda: Activity.objects.count(), ""),
        ("careerposition", "Open positions", "work", lambda: CareerPosition.objects.filter(status="active").count(), ""),
        ("jobapplication", "New applications", "inbox", lambda: JobApplication.objects.filter(status="new").count(), "?status__exact=new"),
        ("customer", "Clients", "handshake", lambda: Customer.objects.count(), ""),
        ("product", "Products", "checkroom", lambda: Product.objects.count(), ""),
        ("galleryimage", "Gallery images", "photo_library", lambda: GalleryImage.objects.count(), ""),
        ("teammember", "Team members", "group", lambda: TeamMember.objects.count(), ""),
        ("testimonial", "Testimonials", "format_quote", lambda: Testimonial.objects.count(), ""),
    ]
    dashboard_stats = []
    for model, label, icon, count, query in stats:
        if not can("view", model):
            continue
        value = count()
        dashboard_stats.append(
            {
                "label": label,
                "value": value,
                "icon": icon,
                "url": _url(model) + query,
                "highlight": model == "jobapplication" and value > 0,
            }
        )

    actions = [
        ("change", "homeherosection", "Home hero", "Slides & headline", "view_carousel", _url("homeherosection")),
        ("add", "activity", "New activity", "Publish news", "add_circle", reverse("admin:hapl_activity_add")),
        ("add", "careerposition", "New position", "Post a job", "person_add", reverse("admin:hapl_careerposition_add")),
        ("change", "productspage", "Products", "Catalogue", "inventory_2", _url("productspage")),
        ("change", "gallerypage", "Gallery", "Photos & videos", "photo_library", _url("gallerypage")),
        ("change", "sitesettings", "Site settings", "Logo, footer, SEO", "settings", _url("sitesettings")),
    ]
    quick_actions = [
        {"label": label, "hint": hint, "icon": icon, "url": url}
        for action, model, label, hint, icon, url in actions
        if can(action, model)
    ]

    context.update(
        {
            "dashboard_stats": dashboard_stats,
            "quick_actions": quick_actions,
            "show_activities": can("view", "activity"),
            "show_positions": can("view", "careerposition"),
            "show_applications": can("view", "jobapplication"),
            "activities_url": _url("activity"),
            "positions_url": _url("careerposition"),
            "applications_url": _url("jobapplication"),
        }
    )
    if context["show_activities"]:
        context["recent_activities"] = Activity.objects.order_by("-activity_date")[:5]
    if context["show_positions"]:
        context["active_positions"] = CareerPosition.objects.filter(status="active").order_by("-posted_at")[:5]
    if context["show_applications"]:
        context["recent_applications"] = (
            JobApplication.objects.select_related("position").order_by("-created_at")[:5]
        )
    return context
