import logging

from django.db import transaction

from hapl.models import (
    SiteSettings,
    NavbarSettings,
    AuditStatus,
    ComplianceCompanyInfo,
    CompanyInfoStat,
    CompanyBuyer,
    ProductionStep,
)
from seeder import data
from seeder.content_factories import (
    SiteSettingsFactory,
    NavbarSettingsFactory,
    HomeHeroSectionFactory,
    HomeIntroductionSectionFactory,
    HomeServicesSectionFactory,
    HomeStatsSectionFactory,
    AboutSectionFactory,
    WhyUsSectionFactory,
    WhyUsFeatureFactory,
    TeamSectionFactory,
    FAQSectionFactory,
    CustomersSectionFactory,
    TestimonialsSectionFactory,
    ContactSectionFactory,
    CareerSectionFactory,
    ActivitiesSectionFactory,
    HomeCarouselSlideFactory,
    HomeIntroductionFeatureFactory,
    ServiceFactory,
    CompanyStatsFactory,
    TeamMemberFactory,
    FAQFactory,
    CustomerFactory,
    TestimonialFactory,
    ContactDataFactory,
    ContactPhoneFactory,
    ContactEmailFactory,
    ContactGroupFactory,
    ContactMemberFactory,
    SocialFactory,
    CareerPositionFactory,
    JobApplicationFactory,
    ActivityFactory,
    ProductsPageFactory,
    ProductCarouselSlideFactory,
    ProductSectionFactory,
    ProductCategoryFactory,
    ProductFactory,
    CompliancePageFactory,
    ComplianceSectionFactory,
    ComplianceCertificateFactory,
    SustainabilityPageFactory,
    SustainabilitySectionFactory,
    SustainabilityCertificateFactory,
    GalleryPageFactory,
    GallerySectionFactory,
    GalleryImageFactory,
)


logger = logging.getLogger(__name__)


# Real audit/certification records from the company's official Audit Status sheet.
AUDIT_RECORDS = [
    {"sl_no": 1, "name": "BSCI", "certificate_number": "23-0222757", "audit_date": "31/10/2023", "expiry_date": "21/10/2027", "status": "Done", "result": "B"},
    {"sl_no": 2, "name": "WRAP", "certificate_number": "130277", "audit_date": "18 & 19 Jun 2025", "expiry_date": "18/07/2026", "status": "Done", "result": "GOLD"},
    {"sl_no": 3, "name": "BETTER WORK", "certificate_number": "3501", "audit_date": "22/06/2025", "expiry_date": "Running", "status": "Running", "result": "2nd Assessment"},
    {"sl_no": 4, "name": "C-TPAT", "certificate_number": "C-TPAT/25003", "audit_date": "28/01/2025", "expiry_date": "28/01/2026", "status": "Done", "result": "Certified"},
    {"sl_no": 5, "name": "GSV", "certificate_number": "A5202027", "audit_date": "27/11/2024", "expiry_date": "17/12/2026", "status": "Done", "result": "Certified"},
    {"sl_no": 6, "name": "RSC (Structural, Electrical & Fire)", "certificate_number": "26255", "audit_date": "25/06/2025", "expiry_date": "Initial", "status": "Running", "result": "Done"},
    {"sl_no": 7, "name": "GOTS", "certificate_number": "24-706234", "audit_date": "19/11/2024", "expiry_date": "27/11/2026", "status": "Done", "result": "Certified"},
    {"sl_no": 8, "name": "RDS", "certificate_number": "24-706231", "audit_date": "19/11/2024", "expiry_date": "27/11/2026", "status": "Done", "result": "Certified"},
    {"sl_no": 9, "name": "OCS", "certificate_number": "24-675249", "audit_date": "30/09/2025", "expiry_date": "29/09/2026", "status": "Done", "result": "Certified"},
    {"sl_no": 10, "name": "RCS", "certificate_number": "24-675261", "audit_date": "30/09/2025", "expiry_date": "29/09/2026", "status": "Done", "result": "Certified"},
    {"sl_no": 11, "name": "GRS", "certificate_number": "25-753792", "audit_date": "06/02/2026", "expiry_date": "06/02/2027", "status": "Done", "result": "Certified"},
    {"sl_no": 12, "name": "Regenagri – Control Union", "certificate_number": "CU1423220REGENAGRI-2025-00066693", "audit_date": "24/06/2025", "expiry_date": "23/06/2026", "status": "Done", "result": "Certified"},
    {"sl_no": 13, "name": "Oekotex Standard 100", "certificate_number": "24.HBD.11684", "audit_date": "30/12/2024", "expiry_date": "30/12/2025", "status": "Applied", "result": "Certified"},
    {"sl_no": 14, "name": "Higg FEM 4.0", "certificate_number": "174627", "audit_date": "07/07/2025", "expiry_date": "31/07/2026", "status": "Done", "result": "Verified"},
    {"sl_no": 15, "name": "ISO 9001:2015 QMS", "certificate_number": "ISO/26010036", "audit_date": "29/04/2026", "expiry_date": "26/04/2029", "status": "Initial Done", "result": "Certified"},
    {"sl_no": 16, "name": "USCTP", "certificate_number": "W6E3GKHR", "audit_date": "01/11/2025", "expiry_date": "31/10/2026", "status": "Applied", "result": "Membership"},
    {"sl_no": 17, "name": "Hugo Boss Social Compliance", "certificate_number": "O-F 26/011 O&J", "audit_date": "29 & 30 Apr 2026", "expiry_date": "29 Apr 2027", "status": "Done", "result": "Satisfied"},
    {"sl_no": 18, "name": "SLCP (Betterwork)", "certificate_number": None, "audit_date": None, "expiry_date": None, "status": "Done", "result": "Not Verified"},
    {"sl_no": 19, "name": "Hugo Boss Environmental Audit (Eurofins)", "certificate_number": None, "audit_date": None, "expiry_date": None, "status": "Done", "result": "Verified"},
    {"sl_no": 20, "name": "Macy's COC Audit (LRQA)", "certificate_number": "314245", "audit_date": None, "expiry_date": None, "status": "Done", "result": "Completed"},
]

# Real company-information content shown in the "Company Information" section.
COMPANY_STATS = [
    {"icon": "ph-calendar-blank", "label": "Established", "value": "1986"},
    {"icon": "ph-ruler", "label": "Area", "value": "219,219 sq ft", "subtext": "13,577 sq m"},
    {"icon": "ph-users-three", "label": "Manpower", "value": "2,400"},
    {"icon": "ph-package", "label": "Capacity", "value": "150,000", "subtext": "Pcs / Month"},
    {"icon": "ph-clock-countdown", "label": "Shifts", "value": "3"},
    {"icon": "ph-rows", "label": "Total Lines", "value": "28"},
]
COMPANY_BUYERS = [
    {"name": "Hugo Boss", "percentage": "60%"},
    {"name": "Marco Polo", "percentage": "15%"},
    {"name": "Macy's", "percentage": "15%"},
    {"name": "Antailor", "percentage": "5%"},
    {"name": "Others", "percentage": "5%"},
]
COMPANY_STEPS = [
    {"name": "Cutting"},
    {"name": "Sewing", "note": "(Quilting, Downfilling)"},
    {"name": "Finishing"},
    {"name": "Packing"},
]


def seed_audits(compliance_page):
    """Pre-populate the 20 real audit/certification records for the compliance page."""
    for record in AUDIT_RECORDS:
        AuditStatus.objects.create(page=compliance_page, **record)
    logger.info("   ↳ Seeded %d audit status records.", len(AUDIT_RECORDS))


def seed_company_info(compliance_page):
    """Pre-populate the admin-managed Company Information section."""
    ComplianceCompanyInfo.objects.create(
        page=compliance_page, eyebrow="At a Glance", title="Company Information"
    )
    for order, stat in enumerate(COMPANY_STATS):
        CompanyInfoStat.objects.create(page=compliance_page, order=order, **stat)
    for order, buyer in enumerate(COMPANY_BUYERS):
        CompanyBuyer.objects.create(page=compliance_page, order=order, **buyer)
    for order, step in enumerate(COMPANY_STEPS):
        ProductionStep.objects.create(page=compliance_page, order=order, **step)
    logger.info("   ↳ Seeded company information section.")


def _delete_all(*factories):
    for f in factories:
        f._meta.model.objects.all().delete()


class Seeder:
    """Base seeder class."""

    def __init__(self, clean=False):
        self.clean = clean

    def run(self):
        raise NotImplementedError

    def clean_data(self):
        """Delete existing data before seeding."""
        raise NotImplementedError


class SiteSeeder(Seeder):
    def clean_data(self):
        # Singletons are updated in place, never deleted.
        logger.info("🧹 Site settings are updated in place.")

    @transaction.atomic
    def run(self):
        logger.info("🌱 Seeding site settings...")
        site = SiteSettings.objects.filter(pk=1).first() or SiteSettingsFactory.create()
        for field, value in data.SITE.items():
            setattr(site, field, value)
        # A database restored without its media folder points at files that
        # no longer exist; drop those so the header shows the text wordmark
        # instead of a broken image.
        for field in ("logo", "site_logo", "logo_light", "favicon", "site_favicon"):
            file = getattr(site, field)
            if file and not file.storage.exists(file.name):
                setattr(site, field, None)
        site.save()
        NavbarSettings.objects.get_or_create(pk=1)
        logger.info("✅ Site settings seeded.")


class HomeSeeder(Seeder):
    def clean_data(self):
        _delete_all(
            HomeCarouselSlideFactory,
            HomeIntroductionFeatureFactory,
            CompanyStatsFactory,
            ServiceFactory,
            HomeHeroSectionFactory,
            HomeIntroductionSectionFactory,
            HomeServicesSectionFactory,
            HomeStatsSectionFactory,
        )
        logger.info("🧹 Home data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Home data...")

        hero = HomeHeroSectionFactory.create(**data.HERO)
        for order, slide in enumerate(data.HERO_SLIDES):
            values = {k: v for k, v in slide.items() if k != "label"}
            HomeCarouselSlideFactory.create(section=hero, order=order, **values)

        intro = HomeIntroductionSectionFactory.create()
        for feature in data.INTRO_FEATURES:
            HomeIntroductionFeatureFactory.create(introduction=intro, **feature)

        services = HomeServicesSectionFactory.create()
        for order, service in enumerate(data.SERVICES):
            ServiceFactory.create(section=services, order=order, **service)

        stats = HomeStatsSectionFactory.create()
        for order, stat in enumerate(data.STATS):
            CompanyStatsFactory.create(section=stats, order=order, **stat)

        logger.info("✅ Home data seeded.")


class AboutSeeder(Seeder):
    def clean_data(self):
        _delete_all(
            TeamMemberFactory,
            FAQFactory,
            WhyUsFeatureFactory,
            AboutSectionFactory,
            WhyUsSectionFactory,
            TeamSectionFactory,
            FAQSectionFactory,
        )
        logger.info("🧹 About data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding About data...")

        AboutSectionFactory.create()

        why = WhyUsSectionFactory.create()
        for order, value in enumerate(data.CORE_VALUES):
            WhyUsFeatureFactory.create(section=why, order=order, **value)

        team = TeamSectionFactory.create()
        for order, member in enumerate(data.MANAGEMENT):
            TeamMemberFactory.create(section=team, order=order, is_management=True, **member)
        for order, member in enumerate(data.STAFF):
            TeamMemberFactory.create(section=team, order=order, is_management=False, **member)

        faq = FAQSectionFactory.create()
        for order, item in enumerate(data.FAQS):
            FAQFactory.create(section=faq, order=order, **item)

        logger.info("✅ About data seeded.")


class CustomerSeeder(Seeder):
    def clean_data(self):
        _delete_all(CustomerFactory, TestimonialFactory, CustomersSectionFactory, TestimonialsSectionFactory)
        logger.info("🧹 Customer data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Customer data...")

        customers = CustomersSectionFactory.create()
        for order, customer in enumerate(data.CUSTOMERS):
            CustomerFactory.create(section=customers, order=order, **customer)

        testimonials = TestimonialsSectionFactory.create()
        for order, testimonial in enumerate(data.TESTIMONIALS):
            TestimonialFactory.create(section=testimonials, order=order, **testimonial)

        logger.info("✅ Customer data seeded.")


class ContactSeeder(Seeder):
    def clean_data(self):
        _delete_all(
            ContactPhoneFactory,
            ContactEmailFactory,
            ContactMemberFactory,
            ContactGroupFactory,
            SocialFactory,
            ContactDataFactory,
            ContactSectionFactory,
        )
        logger.info("🧹 Contact data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Contact data...")

        section = ContactSectionFactory.create()
        contact_data = ContactDataFactory.create(section=section)
        for phone in data.CONTACT_PHONES:
            ContactPhoneFactory.create(contact=contact_data, **phone)
        for email in data.CONTACT_EMAILS:
            ContactEmailFactory.create(contact=contact_data, **email)

        for name, members in data.CONTACT_GROUPS.items():
            group = ContactGroupFactory.create(section=section, name=name)
            for member in members:
                ContactMemberFactory.create(group=group, **member)

        for order, social in enumerate(data.SOCIALS):
            SocialFactory.create(section=section, order=order, **social)

        logger.info("✅ Contact data seeded.")


class CareerSeeder(Seeder):
    def clean_data(self):
        _delete_all(JobApplicationFactory, CareerPositionFactory, CareerSectionFactory)
        logger.info("🧹 Career data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Career data...")

        section = CareerSectionFactory.create()
        for order, position in enumerate(data.POSITIONS):
            created = CareerPositionFactory.create(section=section, order=order, **position)
            # A couple of sample applications per position for the admin.
            JobApplicationFactory.create_batch(2, position=created)

        logger.info("✅ Career data seeded.")


class ActivitiesSeeder(Seeder):
    def clean_data(self):
        _delete_all(ActivityFactory, ActivitiesSectionFactory)
        logger.info("🧹 Activities data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Activities data...")

        section = ActivitiesSectionFactory.create()
        for activity in data.ACTIVITIES:
            ActivityFactory.create(section=section, **activity)

        logger.info("✅ Activities data seeded.")


class ProductsSeeder(Seeder):
    def clean_data(self):
        _delete_all(
            ProductFactory,
            ProductCategoryFactory,
            ProductSectionFactory,
            ProductCarouselSlideFactory,
            ProductsPageFactory,
        )
        logger.info("🧹 Products data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Products data...")

        page = ProductsPageFactory.create()
        for order, alt in enumerate(data.PRODUCT_CAROUSEL):
            ProductCarouselSlideFactory.create(page=page, order=order, alt=alt)
        for order, section in enumerate(data.PRODUCT_SECTIONS):
            ProductSectionFactory.create(page=page, order=order, **section)

        for cat_order, (category_name, products) in enumerate(data.PRODUCT_CATEGORIES.items()):
            category = ProductCategoryFactory.create(page=page, name=category_name, order=cat_order)
            for order, (name, gender, buyer) in enumerate(products):
                ProductFactory.create(category=category, name=name, gender=gender, buyer=buyer, order=order)

        logger.info("✅ Products data seeded.")


class ComplianceSeeder(Seeder):
    def clean_data(self):
        _delete_all(ComplianceSectionFactory, ComplianceCertificateFactory)
        AuditStatus.objects.all().delete()
        ComplianceCompanyInfo.objects.all().delete()
        CompanyInfoStat.objects.all().delete()
        CompanyBuyer.objects.all().delete()
        ProductionStep.objects.all().delete()
        _delete_all(CompliancePageFactory)
        logger.info("🧹 Compliance data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Compliance data...")

        page = CompliancePageFactory.create()
        for order, section in enumerate(data.COMPLIANCE_SECTIONS):
            ComplianceSectionFactory.create(page=page, order=order, **section)
        for order, (name, url) in enumerate(data.COMPLIANCE_CERTIFICATES):
            ComplianceCertificateFactory.create(page=page, order=order, name=name, website_url=url)

        seed_audits(page)
        seed_company_info(page)

        logger.info("✅ Compliance data seeded.")


class SustainabilitySeeder(Seeder):
    def clean_data(self):
        _delete_all(SustainabilitySectionFactory, SustainabilityCertificateFactory, SustainabilityPageFactory)
        logger.info("🧹 Sustainability data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Sustainability data...")

        page = SustainabilityPageFactory.create()
        for order, section in enumerate(data.SUSTAINABILITY_SECTIONS):
            SustainabilitySectionFactory.create(page=page, order=order, **section)
        for order, name in enumerate(data.SUSTAINABILITY_CERTIFICATES):
            SustainabilityCertificateFactory.create(page=page, order=order, name=name)

        logger.info("✅ Sustainability data seeded.")


class GallerySeeder(Seeder):
    def clean_data(self):
        _delete_all(GalleryImageFactory, GallerySectionFactory, GalleryPageFactory)
        logger.info("🧹 Gallery data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Gallery data...")

        page = GalleryPageFactory.create()
        for sec_order, (section_name, captions) in enumerate(data.GALLERY_SECTIONS.items()):
            section = GallerySectionFactory.create(page=page, name=section_name, order=sec_order)
            for order, caption in enumerate(captions):
                GalleryImageFactory.create(section=section, caption=caption, order=order)
        # Videos are left for editors: there are no verified company videos to embed.

        logger.info("✅ Gallery data seeded.")
