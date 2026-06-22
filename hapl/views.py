import logging
from email.utils import formataddr

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from hapl.forms import JobApplicationForm
from hapl.models import (
    HomeHeroSection,
    HomeCarouselSlide,
    HomeIntroductionSection,
    HomeIntroductionFeature,
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
    ContactPhone,
    ContactEmail,
    ContactGroup,
    CareerSection,
    CareerPosition,
    MailSettings,
    ActivitiesSection,
    Activity,
    Social,
    ProductsPage,
    ProductCarouselSlide,
    ProductSection,
    ProductCategory,
    Product,
    CompliancePage,
    ComplianceSection,
    ComplianceCertificate,
    AuditStatus,
    SustainabilityPage,
    SustainabilitySection,
    SustainabilityCertificate,
    GalleryPage,
    GallerySection,
    GalleryImage,
    GalleryVideo,
)


def home(request):
    intro_section = HomeIntroductionSection.objects.first()
    stats_section = HomeStatsSection.objects.first()
    services_section = HomeServicesSection.objects.first()
    why_section = WhyUsSection.objects.first()
    products_page = ProductsPage.objects.first()

    # Build product category previews (name + a representative image)
    products_preview = []
    for category in ProductCategory.objects.filter(page=products_page)[:6]:
        first_product = Product.objects.filter(category=category).first()
        products_preview.append(
            {
                "name": category.name,
                "image": first_product.image.url if first_product else None,
            }
        )

    # Flat product rows for the home "Mens / Ladies Wear" scrollers
    category_ids = ProductCategory.objects.filter(page=products_page).values_list(
        "id", flat=True
    )
    mens_products = Product.objects.filter(
        category_id__in=category_ids, gender="Male"
    )[:8]
    ladies_products = Product.objects.filter(
        category_id__in=category_ids, gender="Female"
    )[:8]

    # First 6 gallery images for the home factory gallery
    gallery_images = GalleryImage.objects.all()[:6]

    return render(
        request,
        "www/home.html",
        {
            "hero": {
                "title": "Welcome to Humana Apparels",
                "section": HomeHeroSection.objects.first(),
                "slides": HomeCarouselSlide.objects.filter(is_active=True),
            },
            "activities": {
                "title": "Our Activities",
                "subtitle": None,
                "items": Activity.objects.filter(is_featured=True)[:3],
            },
            "clients": Customer.objects.filter(is_featured=True),
            "intro": intro_section,
            "intro_features": (
                HomeIntroductionFeature.objects.filter(introduction=intro_section)
                if intro_section
                else []
            ),
            "stats": {
                "title": (
                    stats_section.title if stats_section else "Our Impact in Numbers"
                ),
                "subtitle": stats_section.subtitle if stats_section else None,
                "items": CompanyStats.objects.all(),
            },
            "why": {
                "title": why_section.title if why_section else "Why Humana",
                "subtitle": (
                    why_section.subtitle
                    if why_section
                    else "What makes us a trusted manufacturing partner"
                ),
                # Falls back to services so the section is never empty
                "features": WhyUsFeature.objects.all() or Service.objects.all(),
            },
            "services": {
                "title": services_section.title if services_section else "Our Services",
                "subtitle": services_section.subtitle if services_section else None,
                "items": Service.objects.all(),
            },
            "products_preview": products_preview,
            "mens_products": mens_products,
            "ladies_products": ladies_products,
            "gallery_images": gallery_images,
        },
    )


def about(request):
    about_section = AboutSection.objects.first()
    team_section = TeamSection.objects.first()
    faq_section = FAQSection.objects.first()

    return render(
        request,
        "www/about.html",
        {
            "about": about_section,
            "key_facts": CompanyStats.objects.all()[:4],
            # Evergreen content; promote to a model later if it needs CMS editing
            "core_values": [
                {
                    "icon": "ph-shield-check",
                    "title": "Integrity",
                    "description": "We operate transparently and ethically in every relationship and transaction.",
                },
                {
                    "icon": "ph-medal",
                    "title": "Quality",
                    "description": "Uncompromising standards from raw material to the finished garment.",
                },
                {
                    "icon": "ph-leaf",
                    "title": "Sustainability",
                    "description": "Responsible processes that protect the environment and future generations.",
                },
                {
                    "icon": "ph-users-three",
                    "title": "People First",
                    "description": "A safe, fair and empowering workplace for every member of our team.",
                },
                {
                    "icon": "ph-handshake",
                    "title": "Reliability",
                    "description": "On-time delivery and dependable partnerships our buyers can trust.",
                },
                {
                    "icon": "ph-lightbulb",
                    "title": "Innovation",
                    "description": "Continuously improving through technology and smarter ways of working.",
                },
            ],
            "team": {
                "title": team_section.title if team_section else "Our Team",
                "subtitle": team_section.subtitle if team_section else None,
                "management": TeamMember.objects.filter(is_management=True),
                "staff": TeamMember.objects.filter(is_management=False),
            },
            "faq": {
                "title": (
                    faq_section.title if faq_section else "Frequently Asked Questions"
                ),
                "subtitle": (
                    faq_section.subtitle
                    if faq_section
                    else "Get answers to common questions about our services"
                ),
                "faqs": FAQ.objects.all(),
            },
        },
    )


def customers(request):
    customers_section = CustomersSection.objects.first()
    testimonials_section = TestimonialsSection.objects.first()

    featured_testimonial = (
        Testimonial.objects.filter(is_featured=True).first()
        or Testimonial.objects.first()
    )

    return render(
        request,
        "www/customers.html",
        {
            "clients_data": {
                "title": (
                    customers_section.title
                    if customers_section
                    else "Trusted by Global Fashion Brands"
                ),
                "subtitle": (
                    customers_section.subtitle
                    if customers_section
                    else "Partnering with industry leaders in sustainable fashion manufacturing"
                ),
                "clients": Customer.objects.all(),
            },
            "testimonials": {
                "title": (
                    testimonials_section.title
                    if testimonials_section
                    else "What Our Clients Say"
                ),
                "subtitle": (
                    testimonials_section.subtitle
                    if testimonials_section
                    else "Read what our clients have to say about us"
                ),
                "featured": featured_testimonial,
                "testimonials": Testimonial.objects.all(),
            },
        },
    )


def contact(request):
    contact_section = ContactSection.objects.first()
    contact_data = ContactData.objects.first()
    contact_groups = ContactGroup.objects.all()
    socials = Social.objects.all()

    phones = {"phone": [], "whatsapp": []}

    if contact_data:
        for phone in ContactPhone.objects.filter(contact=contact_data):
            phones[phone.type].append(phone.number)

    emails = []
    if contact_data:
        emails = [
            email.email for email in ContactEmail.objects.filter(contact=contact_data)
        ]

    return render(
        request,
        "www/contact.html",
        {
            "contact": {
                "title": contact_section.title if contact_section else "Contact Us",
                "subtitle": (
                    contact_section.subtitle
                    if contact_section
                    else "Get in touch with our team"
                ),
                "office": {
                    "title": (
                        contact_data.office_title if contact_data else "Our Office"
                    ),
                    "subtitle": contact_data.office_subtitle if contact_data else None,
                    "image": contact_data.office_image if contact_data else None,
                    "contacts": {
                        "phones": phones["phone"],
                        "whatsapp": phones["whatsapp"],
                        "emails": emails,
                        "fax": contact_data.fax if contact_data else None,
                    },
                },
                "groups": contact_groups,
                "socials": socials,
                "map": {
                    "title": contact_data.map_title if contact_data else "Find Us",
                    "subtitle": contact_data.map_subtitle if contact_data else None,
                    "image": contact_data.map_image if contact_data else None,
                    "map_url": contact_data.map_url if contact_data else None,
                    "address": contact_data.address if contact_data else None,
                },
            }
        },
    )


def activities(request):
    activities_section = ActivitiesSection.objects.first()

    return render(
        request,
        "www/activities.html",
        {
            "activities": {
                "title": (
                    activities_section.title
                    if activities_section
                    else "Our Activities"
                ),
                "subtitle": (
                    activities_section.subtitle
                    if activities_section
                    else "CSR, compliance and community initiatives from across Humana Apparels"
                ),
                "items": Activity.objects.all().order_by("-activity_date"),
            }
        },
    )


logger = logging.getLogger(__name__)


def career(request):
    career_section = CareerSection.objects.first()
    # Each position retains its pk so the template can link to the apply page.
    active_positions = CareerPosition.objects.filter(status="active")

    return render(
        request,
        "www/career.html",
        {
            "career": {
                "title": (
                    career_section.title if career_section else "Career Opportunities"
                ),
                "subtitle": (
                    career_section.subtitle
                    if career_section
                    else "Join our team and grow with us"
                ),
                "positions": active_positions,
            }
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
            "position": position,
            "form": form,
            "submitted": request.GET.get("submitted") == "1",
        },
    )


def products(request):
    products_page = ProductsPage.objects.first()

    context = {
        "carousel": ProductCarouselSlide.objects.filter(page=products_page),
        "sections": ProductSection.objects.filter(page=products_page),
        "product_portfolio": [],
    }

    # Build the product portfolio structure with pre-processed gender data
    for category in ProductCategory.objects.filter(page=products_page):
        portfolio_item = {
            "section": category.name,
            "has_male": False,
            "has_female": False,
            "has_other": False,
            "male_products": [],
            "female_products": [],
            "other_products": [],
        }

        # Categorize products by gender
        for product in Product.objects.filter(category=category):
            product_data = {
                "name": product.name,
                "image": product.image.url,
                "buyer": product.buyer,
            }

            if product.gender == "Male":
                portfolio_item["has_male"] = True
                portfolio_item["male_products"].append(product_data)
            elif product.gender == "Female":
                portfolio_item["has_female"] = True
                portfolio_item["female_products"].append(product_data)
            else:
                portfolio_item["has_other"] = True
                portfolio_item["other_products"].append(product_data)

        context["product_portfolio"].append(portfolio_item)

    return render(request, "www/products.html", context)


def complience(request):
    compliance_page = CompliancePage.objects.first()

    complience_data = {
        "sections": [],
        "certificates": [],
        "audits": AuditStatus.objects.filter(page=compliance_page).order_by("sl_no"),
    }

    # Add sections
    for section in ComplianceSection.objects.filter(page=compliance_page):
        complience_data["sections"].append(
            {
                "title": section.title,
                "description": section.description,
                "image": section.image.url,
            }
        )

    # Add certificates
    for certificate in ComplianceCertificate.objects.filter(page=compliance_page):
        complience_data["certificates"].append(
            {"name": certificate.name, "image": certificate.image.url}
        )

    return render(request, "www/complience.html", {"complience_data": complience_data})


def sustainability(request):
    sustainability_page = SustainabilityPage.objects.first()

    sustainability_data = {"sections": [], "certificates": []}

    # Add sections
    for section in SustainabilitySection.objects.filter(page=sustainability_page):
        sustainability_data["sections"].append(
            {
                "title": section.title,
                "description": section.description,
                "image": section.image.url,
            }
        )

    # Add certificates
    for certificate in SustainabilityCertificate.objects.filter(
        page=sustainability_page
    ):
        sustainability_data["certificates"].append(
            {"name": certificate.name, "image": certificate.image.url}
        )

    return render(
        request, "www/sustainability.html", {"sustainability_data": sustainability_data}
    )


def gallery(request):
    gallery_page = GalleryPage.objects.first()

    # Initialize dictionaries to store images and videos by section
    images_by_section = {}
    videos_by_section = {}

    # Organize images by section
    for section in GallerySection.objects.filter(page=gallery_page):
        section_name = section.name

        # Get images for this section
        if section_name not in images_by_section:
            images_by_section[section_name] = []

        for image in GalleryImage.objects.filter(section=section):
            images_by_section[section_name].append(
                {
                    "caption": image.caption,
                    "url": image.image.url,
                    "section": section_name,
                }
            )

        # Get videos for this section
        if section_name not in videos_by_section:
            videos_by_section[section_name] = []

        for video in GalleryVideo.objects.filter(section=section):
            videos_by_section[section_name].append(
                {
                    "caption": video.caption,
                    "youtube_url": video.youtube_url,
                    "section": section_name,
                }
            )

    context = {
        "gallery_data": {
            "images_by_section": images_by_section,
            "videos_by_section": videos_by_section,
        }
    }

    return render(request, "www/gallery.html", context)
