import logging
from email.utils import formataddr

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from hapl.forms import JobApplicationForm
from hapl.models import (
    HomeHeroSection,
    HomeCarouselSlide,
    HomeIntroductionSection,
    HomeServicesSection,
    Service,
    HomeStatsSection,
    CompanyStats,
    AboutSection,
    WhyUsSection,
    WhyUsFeature,
    TeamSection,
    TeamMember,
    FAQSection,
    FAQ,
    CustomersSection,
    Customer,
    TestimonialsSection,
    Testimonial,
    ContactSection,
    ContactData,
    ContactGroup,
    Social,
    CareerSection,
    CareerPosition,
    MailSettings,
    ActivitiesSection,
    Activity,
    ProductsPage,
    ProductCategory,
    Product,
    CompliancePage,
    ComplianceCompanyInfo,
    ComplianceCertificate,
    SustainabilityPage,
    GalleryPage,
    GallerySection,
    GalleryImage,
)


logger = logging.getLogger(__name__)


def _page(obj, model):
    """Templates get an unsaved blank instance instead of None so lookups such
    as `page.banner_title|default:page.title` never fail on an empty database."""
    return obj if obj is not None else model()


def _stats():
    """Home stats in display order, scoped to the first stats section when one
    exists (legacy rows without a section are still shown when none does)."""
    section = HomeStatsSection.objects.order_by("id").first()
    stats = CompanyStats.objects.order_by("order", "id")
    if section is not None:
        stats = stats.filter(section=section)
    return section, list(stats)


def home(request):
    hero = (
        HomeHeroSection.objects.filter(is_active=True)
        .prefetch_related(
            Prefetch(
                "slides",
                queryset=HomeCarouselSlide.objects.filter(is_active=True).order_by(
                    "order", "id"
                ),
                to_attr="active_slides",
            )
        )
        .order_by("id")
        .first()
    )
    intro = (
        HomeIntroductionSection.objects.prefetch_related("features")
        .order_by("id")
        .first()
    )
    services_section = HomeServicesSection.objects.order_by("id").first()
    services = Service.objects.order_by("order", "id")
    if services_section is not None:
        services = services.filter(section=services_section)
    stats_section, stats = _stats()

    activities_section = ActivitiesSection.objects.order_by("id").first()
    activities = list(
        Activity.objects.filter(is_featured=True).order_by("-activity_date")[:3]
    )
    customers_section = CustomersSection.objects.order_by("id").first()
    clients = list(Customer.objects.filter(is_featured=True).order_by("order", "id"))
    # Each half of the infinite marquee must be wider than the viewport, so
    # short client lists are repeated (screen readers only get the first copy).
    repeat = -(-12 // len(clients)) if clients else 0

    # Product categories with one representative image each (2 queries).
    products_page = ProductsPage.objects.order_by("id").first()
    categories = []
    if products_page is not None:
        categories = list(
            ProductCategory.objects.filter(page=products_page)
            .order_by("order", "id")
            .prefetch_related(
                Prefetch("products", queryset=Product.objects.order_by("order", "id"))
            )[:6]
        )
    products_preview = []
    for category in categories:
        items = list(category.products.all())
        products_preview.append(
            {"name": category.name, "count": len(items), "image": items[0].image if items else None}
        )

    gallery_page = GalleryPage.objects.order_by("id").first()
    gallery_images = list(
        GalleryImage.objects.select_related("section").order_by("section__order", "order", "id")[:6]
    )

    return render(
        request,
        "www/home.html",
        {
            "hero": hero,
            "slides": hero.active_slides if hero else [],
            "intro": intro,
            "intro_features": list(intro.features.all()) if intro else [],
            "services_section": services_section,
            "services": list(services),
            "stats_section": stats_section,
            "stats": stats,
            "activities_section": activities_section,
            "activities": activities,
            "customers_section": customers_section,
            "clients": clients,
            "marquee_clients": clients * repeat,
            "products_page": products_page,
            "products_preview": products_preview,
            "gallery_page": gallery_page,
            "gallery_images": gallery_images,
        },
    )


def about(request):
    why_section = (
        WhyUsSection.objects.prefetch_related(
            Prefetch("features", queryset=WhyUsFeature.objects.order_by("order", "id"))
        )
        .order_by("id")
        .first()
    )
    members = list(TeamMember.objects.order_by("order", "id"))
    _, stats = _stats()

    return render(
        request,
        "www/about.html",
        {
            "page": _page(AboutSection.objects.order_by("id").first(), AboutSection),
            "key_facts": stats[:4],
            "why_section": why_section,
            "core_values": list(why_section.features.all()) if why_section else [],
            "team_section": TeamSection.objects.order_by("id").first(),
            "management": [m for m in members if m.is_management],
            "staff": [m for m in members if not m.is_management],
            "faq_section": FAQSection.objects.order_by("id").first(),
            "faqs": list(FAQ.objects.order_by("order", "id")),
        },
    )


def customers(request):
    testimonials = list(Testimonial.objects.order_by("order", "id"))
    featured = next((t for t in testimonials if t.is_featured), None) or (
        testimonials[0] if testimonials else None
    )

    return render(
        request,
        "www/customers.html",
        {
            "page": _page(CustomersSection.objects.order_by("id").first(), CustomersSection),
            "clients": list(Customer.objects.order_by("order", "id")),
            "testimonials_section": TestimonialsSection.objects.order_by("id").first(),
            "featured_testimonial": featured,
            "testimonials": [t for t in testimonials if t != featured],
        },
    )


def contact(request):
    page = ContactSection.objects.order_by("id").first()
    contact_data = (
        ContactData.objects.prefetch_related("contactphones", "contactemails")
        .order_by("id")
        .first()
    )

    phones, whatsapp, emails = [], [], []
    if contact_data:
        for phone in contact_data.contactphones.all():
            (whatsapp if phone.type == "whatsapp" else phones).append(phone.number)
        emails = [email.email for email in contact_data.contactemails.all()]

    return render(
        request,
        "www/contact.html",
        {
            "page": _page(page, ContactSection),
            "contact_data": contact_data,
            "phones": phones,
            "whatsapp": whatsapp,
            "emails": emails,
            "groups": list(
                ContactGroup.objects.prefetch_related("members").order_by("id")
            ),
            "socials": list(Social.objects.order_by("order", "id")),
        },
    )


def activities(request):
    items = list(Activity.objects.order_by("-activity_date", "-id"))
    featured = next((a for a in items if a.is_featured), None) or (
        items[0] if items else None
    )

    return render(
        request,
        "www/activities.html",
        {
            "page": _page(ActivitiesSection.objects.order_by("id").first(), ActivitiesSection),
            "featured": featured,
            "items": [a for a in items if a != featured],
        },
    )


def career(request):
    return render(
        request,
        "www/career.html",
        {
            "page": _page(CareerSection.objects.order_by("id").first(), CareerSection),
            # Each position retains its pk so the template can link to the apply page.
            "positions": list(
                CareerPosition.objects.filter(status="active").order_by("order", "-posted_at")
            ),
        },
    )


def _send_application_emails(application, position):
    """Send applicant confirmation + admin notification, driven by the
    admin-editable MailSettings. SMTP credentials still come from settings/env;
    only the recipient address, sender display name and the on/off toggles are
    DB-configurable. Each send is isolated so a mail failure never breaks the
    submission and one failing send does not prevent the other."""
    mail_settings = MailSettings.load()
    # Sender display name (DB) combined with the configured SMTP from-address.
    from_email = formataddr((mail_settings.sender_name, settings.DEFAULT_FROM_EMAIL))

    # Confirmation to the applicant
    if mail_settings.send_applicant_confirmation:
        try:
            send_mail(
                subject=f"Application received — {position.title}",
                message=(
                    f"Hi {application.full_name},\n\n"
                    f"Thank you for applying for the {position.title} position at "
                    f"Humana Apparels Ltd. We've received your application and our "
                    f"team will review it shortly.\n\n"
                    f"Best regards,\n"
                    f"{mail_settings.sender_name}"
                ),
                from_email=from_email,
                recipient_list=[application.email],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                "Failed to send applicant confirmation email for application %s",
                application.pk,
            )

    # Notification to the careers inbox — no resume/PII in the body itself.
    if mail_settings.send_admin_notification:
        try:
            send_mail(
                subject=f"New job application — {position.title}",
                message=(
                    f"A new application has been submitted.\n\n"
                    f"Applicant: {application.full_name}\n"
                    f"Position: {position.title}\n\n"
                    f"Open the Django admin to view full details and download the resume."
                ),
                from_email=from_email,
                recipient_list=[mail_settings.career_notification_email],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                "Failed to send admin notification email for application %s",
                application.pk,
            )


def career_apply(request, position_id):
    # Only active positions accept applications; anything else is a 404.
    position = get_object_or_404(CareerPosition, pk=position_id, status="active")

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.position = position
            application.save()

            # Email is best-effort: a failure here must not break submission.
            _send_application_emails(application, position)

            # Post/Redirect/Get so a refresh won't resubmit the application.
            url = reverse("career_apply", args=[position.id])
            return redirect(f"{url}?submitted=1")
    else:
        form = JobApplicationForm()

    return render(
        request,
        "www/career_apply.html",
        {
            "page": _page(CareerSection.objects.order_by("id").first(), CareerSection),
            "position": position,
            "form": form,
            "submitted": request.GET.get("submitted") == "1",
        },
    )


def products(request):
    page = (
        ProductsPage.objects.prefetch_related(
            "carousel_slides",
            "sections",
            Prefetch(
                "categories",
                queryset=ProductCategory.objects.order_by("order", "id").prefetch_related(
                    Prefetch("products", queryset=Product.objects.order_by("order", "id"))
                ),
            ),
        )
        .order_by("id")
        .first()
    )

    carousel, sections, portfolio = [], [], []
    if page is not None:
        carousel = list(page.carousel_slides.all())
        sections = list(page.sections.all())
        # One entry per category with products pre-split by gender for the tabs.
        for category in page.categories.all():
            products_ = list(category.products.all())
            groups = [
                ("male", [p for p in products_ if p.gender == "Male"]),
                ("female", [p for p in products_ if p.gender == "Female"]),
                ("other", [p for p in products_ if p.gender not in ("Male", "Female")]),
            ]
            portfolio.append(
                {
                    "id": category.id,
                    "name": category.name,
                    "products": products_,
                    "genders": [key for key, items in groups if items],
                }
            )

    return render(
        request,
        "www/products.html",
        {
            "page": _page(page, ProductsPage),
            "carousel": carousel,
            "sections_before": [s for s in sections if not s.after_products],
            "sections_after": [s for s in sections if s.after_products],
            "portfolio": portfolio,
        },
    )


def complience(request):
    page = (
        CompliancePage.objects.select_related("company_info")
        .prefetch_related(
            "audits",
            "sections",
            "company_stats",
            "buyers",
            "production_steps",
            Prefetch(
                "certificates",
                queryset=ComplianceCertificate.objects.filter(is_active=True).order_by(
                    "order", "id"
                ),
            ),
        )
        .order_by("id")
        .first()
    )

    context = {
        "page": page,
        "audits": [],
        "sections": [],
        "certificates": [],
        "company_info": None,
        "company_stats": [],
        "buyers": [],
        "production_steps": [],
    }
    if page is not None:
        try:
            context["company_info"] = page.company_info
        except ComplianceCompanyInfo.DoesNotExist:
            context["company_info"] = None
        context.update(
            audits=list(page.audits.all()),
            sections=list(page.sections.all()),
            certificates=list(page.certificates.all()),
            company_stats=list(page.company_stats.all()),
            buyers=list(page.buyers.all()),
            production_steps=list(page.production_steps.all()),
        )

    context["page"] = _page(page, CompliancePage)
    return render(request, "www/complience.html", context)


def sustainability(request):
    page = (
        SustainabilityPage.objects.prefetch_related("sections", "certificates")
        .order_by("id")
        .first()
    )
    sections = list(page.sections.all()) if page else []
    certificates = list(page.certificates.all()) if page else []

    return render(
        request,
        "www/sustainability.html",
        {
            "page": _page(page, SustainabilityPage),
            "sections": sections,
            "certificates": certificates,
            # Banner image falls back to the first chapter's photo.
            "banner_image": (page.banner_image if page and page.banner_image else None)
            or (sections[0].image if sections and sections[0].image else None),
        },
    )


def gallery(request):
    page = GalleryPage.objects.order_by("id").first()
    sections = list(
        GallerySection.objects.filter(page=page)
        .order_by("order", "id")
        .prefetch_related("images", "videos")
    ) if page else []

    images, videos = [], []
    for section in sections:
        for image in section.images.all():
            images.append({"section": section, "image": image})
        for video in section.videos.all():
            videos.append({"section": section, "video": video})

    return render(
        request,
        "www/gallery.html",
        {
            "page": _page(page, GalleryPage),
            # Only sections that actually have images get a filter tab.
            "image_sections": [s for s in sections if any(i["section"] == s for i in images)],
            "images": images,
            "videos": videos,
        },
    )
