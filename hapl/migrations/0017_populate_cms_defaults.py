"""Move copy that used to be hard-coded in templates/views into the database.

Only empty fields are filled, so values an editor already set are never
overwritten. The migration is safe to run on an empty database (it creates the
hero and site-settings rows) and on a populated one (it fills the gaps and
links orphaned slides/stats to their section).
"""

import re

from django.db import migrations


HERO_DEFAULTS = {
    "badge_text": "Premier Garment Manufacturer",
    "title": "Quality Apparel, Crafted Responsibly",
    "highlight_word": "Crafted Responsibly",
    "subtitle": (
        "Delivering compliant, sustainable garments to global brands from our "
        "facility in Bangladesh."
    ),
    "cta_primary_text": "Explore Products",
    "cta_primary_url": "/products/",
    "cta_secondary_text": "Contact Us",
    "cta_secondary_url": "/contact/",
    "bottom_label": "Humana Apparels Ltd",
    "bottom_link_text": "Inside our factory",
    "bottom_link_url": "/gallery/",
}

SITE_DEFAULTS = {
    "header_cta_text": "Get in Touch",
    "header_cta_url": "/contact/",
    "footer_description": (
        "A compliant, sustainability-driven garment manufacturer delivering "
        "quality apparel to global brands from Bangladesh."
    ),
    "footer_address": "Dhaka, Bangladesh",
    "footer_email": "info@humanaapparels.com",
    "footer_links_title": "Quick Links",
    "footer_contact_title": "Get in Touch",
    "footer_social_title": "Follow Us",
    "meta_title": "Humana Apparels Ltd — Premier Garment Manufacturer",
    "meta_description": (
        "Humana Apparels Ltd — a compliant, sustainability-driven garment "
        "manufacturer in Bangladesh delivering quality apparel to global brands."
    ),
}

LEGACY_SOCIALS = (
    ("facebook_url", "Facebook", "ph-facebook-logo"),
    ("linkedin_url", "LinkedIn", "ph-linkedin-logo"),
    ("instagram_url", "Instagram", "ph-instagram-logo"),
    ("youtube_url", "YouTube", "ph-youtube-logo"),
    ("twitter_url", "X / Twitter", "ph-x-logo"),
)

# Previously a Python list in hapl/views.py `about()`.
CORE_VALUES = (
    ("ph-shield-check", "Integrity", "We operate transparently and ethically in every relationship and transaction."),
    ("ph-medal", "Quality", "Uncompromising standards from raw material to the finished garment."),
    ("ph-leaf", "Sustainability", "Responsible processes that protect the environment and future generations."),
    ("ph-users-three", "People First", "A safe, fair and empowering workplace for every member of our team."),
    ("ph-handshake", "Reliability", "On-time delivery and dependable partnerships our buyers can trust."),
    ("ph-lightbulb", "Innovation", "Continuously improving through technology and smarter ways of working."),
)

SECTION_DEFAULTS = {
    "HomeIntroductionSection": {
        "eyebrow": "Who We Are",
        "cta_text": "Learn More",
        "cta_url": "/about/",
    },
    "HomeServicesSection": {"eyebrow": "What We Offer"},
    "HomeStatsSection": {"title": "Our Impact in Numbers"},
    "AboutSection": {"eyebrow": "Company Overview", "banner_title": "About Us"},
    "WhyUsSection": {"eyebrow": "What Drives Us", "title": "Our Core Values"},
    "TeamSection": {"eyebrow": "Leadership"},
    "FAQSection": {"eyebrow": "Got Questions?"},
    "CustomersSection": {"eyebrow": "Trusted By"},
    "TestimonialsSection": {"eyebrow": "Kind Words"},
    "ContactSection": {
        "groups_title": "Key Contacts",
        "groups_empty_text": "We'd love to hear from you — reach us using the details on the left.",
        "socials_title": "Connect With Us",
    },
    "CareerSection": {
        "positions_title": "Open Positions",
        "positions_empty_text": "There are no open positions at the moment. Please check back later.",
    },
    "ActivitiesSection": {"eyebrow": "Our Activities"},
    "ProductsPage": {
        "banner_title": "Our Products",
        "portfolio_eyebrow": "What We Make",
        "portfolio_title": "Product Portfolio",
        "cta_title": "Looking for a manufacturing partner?",
        "cta_text": "Tell us about your product and we'll show you what Humana Apparels can deliver.",
        "cta_button_text": "Contact Us",
        "cta_button_url": "/contact/",
    },
    "CompliancePage": {
        "eyebrow": "Compliance Documentation",
        "banner_title": "Our Compliance & Certifications",
        "banner_subtitle": "Committed to global standards in social, environmental and quality compliance.",
        "audit_eyebrow": "Accredited & Audited",
        "audit_title": "Audit Status",
        "audit_description": (
            "Current status of all social, environmental, security and quality "
            "certifications held by Humana Apparels Ltd."
        ),
        "standards_title": "Standards & Code of Conduct",
        "standards_description": "The frameworks and practices we are held accountable to, documented for review.",
        "certificates_eyebrow": "Accredited & Audited",
        "certificates_title": "Our Certifications",
        "cta_title": "Need our compliance documentation?",
        "cta_text": "Request audit reports, certification copies or any compliance-related details from our team.",
        "cta_button_text": "Request Documentation",
        "cta_button_url": "/contact/",
    },
    "SustainabilityPage": {
        "eyebrow": "Our Sustainability Journey",
        "banner_title": "Manufacturing with the planet in mind.",
        "banner_subtitle": (
            "From cleaner production to responsible sourcing, every step we take "
            "is a commitment to lighter footprints and brighter communities."
        ),
        "certificates_title": "Recognized By",
        "cta_title": "Let's build a greener supply chain.",
        "cta_text": "Partner with a manufacturer that treats sustainability as a journey, not a checkbox.",
        "cta_button_text": "Start the Conversation",
        "cta_button_url": "/contact/",
    },
    "GalleryPage": {
        "banner_title": "Gallery",
        "all_tab_label": "All",
        "videos_title": "Videos",
    },
}

STAT_RE = re.compile(r"^\s*(?P<prefix>[^\d]{0,10}?)\s*(?P<number>\d[\d,]*)(?P<suffix>.*?)\s*$")


def _fill(obj, values):
    """Set only the fields that are currently empty; return True if changed."""
    changed = False
    for field, value in values.items():
        if getattr(obj, field) in (None, ""):
            setattr(obj, field, value)
            changed = True
    if changed:
        obj.save()
    return changed


def _alive(model):
    return model.objects.filter(deleted__isnull=True)


def parse_stat_value(raw):
    """'2,400+' -> ('', 2400, '+'); '$5M' -> ('$', 5, 'M'); '1.5M' -> None."""
    match = STAT_RE.match(raw or "")
    if not match:
        return None
    suffix = match.group("suffix").strip()
    if re.match(r"^[.,]?\d", suffix) or len(suffix) > 10:
        return None
    return (
        match.group("prefix").strip(),
        int(match.group("number").replace(",", "")),
        suffix,
    )


def populate(apps, schema_editor):
    HomeHeroSection = apps.get_model("hapl", "HomeHeroSection")
    HomeCarouselSlide = apps.get_model("hapl", "HomeCarouselSlide")
    HomeStatsSection = apps.get_model("hapl", "HomeStatsSection")
    CompanyStats = apps.get_model("hapl", "CompanyStats")
    SiteSettings = apps.get_model("hapl", "SiteSettings")
    ContactSection = apps.get_model("hapl", "ContactSection")
    ContactData = apps.get_model("hapl", "ContactData")
    ContactPhone = apps.get_model("hapl", "ContactPhone")
    ContactEmail = apps.get_model("hapl", "ContactEmail")
    Social = apps.get_model("hapl", "Social")
    WhyUsSection = apps.get_model("hapl", "WhyUsSection")
    WhyUsFeature = apps.get_model("hapl", "WhyUsFeature")
    ProductSection = apps.get_model("hapl", "ProductSection")

    # --- Hero ---
    hero = _alive(HomeHeroSection).order_by("id").first()
    if hero is None:
        hero = HomeHeroSection.objects.create(**HERO_DEFAULTS)
    else:
        defaults = dict(HERO_DEFAULTS)
        # Only highlight the default phrase when the default title is used.
        if hero.title and "highlight_word" in defaults:
            defaults.pop("highlight_word")
        _fill(hero, defaults)
    HomeCarouselSlide.objects.filter(section__isnull=True).update(section=hero)
    for slide in HomeCarouselSlide.objects.filter(alt_text__isnull=True):
        if slide.title:
            slide.alt_text = slide.title[:200]
            slide.save(update_fields=["alt_text"])

    # --- Stats: value -> number/prefix/suffix, title -> label ---
    stats_section = _alive(HomeStatsSection).order_by("id").first()
    if stats_section is not None:
        CompanyStats.objects.filter(section__isnull=True).update(section=stats_section)
    for index, stat in enumerate(CompanyStats.objects.order_by("id")):
        update = {}
        if stat.number is None:
            parsed = parse_stat_value(stat.value)
            if parsed:
                update["prefix"], update["number"], update["suffix"] = parsed
        if not stat.label and stat.title:
            update["label"] = stat.title[:150]
        if stat.order == 0:
            update["order"] = index
        if update:
            CompanyStats.objects.filter(pk=stat.pk).update(**update)

    # --- Site settings ---
    site = SiteSettings.objects.filter(pk=1).first() or SiteSettings.objects.first()
    if site is None:
        site = SiteSettings.objects.create(pk=1)
    site_defaults = dict(SITE_DEFAULTS)
    contact_data = _alive(ContactData).order_by("id").first()
    if contact_data is not None:
        if contact_data.address:
            site_defaults["footer_address"] = contact_data.address
        phone = (
            ContactPhone.objects.filter(contact=contact_data, type="phone")
            .order_by("-is_primary", "id")
            .first()
        )
        if phone:
            site_defaults["footer_phone"] = phone.number
        email = (
            ContactEmail.objects.filter(contact=contact_data)
            .order_by("-is_primary", "id")
            .first()
        )
        if email:
            site_defaults["footer_email"] = email.email
    _fill(site, site_defaults)

    # Legacy SiteSettings social URL fields -> the shared Social model.
    contact_section = _alive(ContactSection).order_by("id").first()
    next_order = Social.objects.count()
    for field, name, icon in LEGACY_SOCIALS:
        url = getattr(site, field)
        if url and not Social.objects.filter(url=url).exists():
            Social.objects.create(
                section=contact_section, name=name, url=url, icon=icon, order=next_order
            )
            next_order += 1

    # --- Section / page copy ---
    for model_name, values in SECTION_DEFAULTS.items():
        model = apps.get_model("hapl", model_name)
        for obj in _alive(model):
            _fill(obj, values)

    for section in ProductSection.objects.filter(eyebrow__isnull=True):
        section.eyebrow = "More" if section.after_products else "Capabilities"
        section.save(update_fields=["eyebrow"])

    # --- Core values (previously hard-coded in views.about) ---
    if not WhyUsFeature.objects.exists():
        why = _alive(WhyUsSection).order_by("id").first()
        if why is None:
            why = WhyUsSection.objects.create(**SECTION_DEFAULTS["WhyUsSection"])
        for order, (icon, title, description) in enumerate(CORE_VALUES):
            WhyUsFeature.objects.create(
                section=why, icon=icon, title=title, description=description, order=order
            )


class Migration(migrations.Migration):

    dependencies = [
        ("hapl", "0016_cms_fields_and_ordering"),
    ]

    operations = [
        migrations.RunPython(populate, migrations.RunPython.noop),
    ]
