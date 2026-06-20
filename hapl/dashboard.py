from hapl.models import (
    Activity,
    CareerPosition,
    Customer,
    TeamMember,
    Product,
    GalleryImage,
    Testimonial,
    FAQ,
)


def dashboard_callback(request, context):
    """Inject stat cards and recent-activity data into the admin dashboard."""
    context.update(
        {
            "dashboard_stats": [
                {
                    "label": "Activities",
                    "value": Activity.objects.count(),
                    "icon": "volunteer_activism",
                    "color": "amber",
                    "url": "/admin/hapl/activitiessection/",
                },
                {
                    "label": "Active Jobs",
                    "value": CareerPosition.objects.filter(status="active").count(),
                    "icon": "work",
                    "color": "green",
                    "url": "/admin/hapl/careersection/",
                },
                {
                    "label": "Clients",
                    "value": Customer.objects.count(),
                    "icon": "handshake",
                    "color": "blue",
                    "url": "/admin/hapl/customerssection/",
                },
                {
                    "label": "Team Members",
                    "value": TeamMember.objects.count(),
                    "icon": "group",
                    "color": "purple",
                    "url": "/admin/hapl/teamsection/",
                },
                {
                    "label": "Products",
                    "value": Product.objects.count(),
                    "icon": "inventory_2",
                    "color": "orange",
                    "url": "/admin/hapl/productspage/",
                },
                {
                    "label": "Gallery Images",
                    "value": GalleryImage.objects.count(),
                    "icon": "photo_library",
                    "color": "pink",
                    "url": "/admin/hapl/gallerypage/",
                },
                {
                    "label": "Testimonials",
                    "value": Testimonial.objects.count(),
                    "icon": "format_quote",
                    "color": "teal",
                    "url": "/admin/hapl/testimonialssection/",
                },
                {
                    "label": "FAQs",
                    "value": FAQ.objects.count(),
                    "icon": "help",
                    "color": "red",
                    "url": "/admin/hapl/faqsection/",
                },
            ],
            "recent_activities": Activity.objects.order_by("-activity_date")[:5],
            "active_positions": CareerPosition.objects.filter(
                status="active"
            ).order_by("-posted_at")[:5],
        }
    )
    return context
