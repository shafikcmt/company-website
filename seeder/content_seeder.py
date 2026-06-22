import random
import logging
from datetime import date
from django.db import transaction
from hapl.models import AuditStatus
from seeder.content_factories import (
    HomeHeroSectionFactory,
    HomeIntroductionSectionFactory,
    HomeServicesSectionFactory,
    HomeStatsSectionFactory,
    AboutSectionFactory,
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
    GalleryVideoFactory,
)


logger = logging.getLogger(__name__)


# Real demo content for the Activities feature (CSR / compliance / community).
SAMPLE_ACTIVITIES = [
    {
        "tag": "Compliance",
        "title": "BSCI Social Audit Completed Successfully",
        "excerpt": (
            "Our facility in Gorai, Mirzapur successfully completed its latest "
            "BSCI social compliance audit, reaffirming our commitment to ethical "
            "labor practices."
        ),
        "activity_date": date(2026, 6, 2),
    },
    {
        "tag": "Sustainability",
        "title": "GOTS-Certified Organic Cotton Line Launched",
        "excerpt": (
            "We've expanded our production capability with a new GOTS-certified "
            "organic cotton line, supporting our partner brands' sustainability "
            "goals."
        ),
        "activity_date": date(2026, 5, 15),
    },
    {
        "tag": "Community",
        "title": "Worker Welfare Training Program",
        "excerpt": (
            "Ongoing skills and welfare training sessions for our workforce, "
            "reflecting our commitment to worker development under the Better "
            "Work program."
        ),
        "activity_date": date(2026, 4, 21),
    },
]


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


def seed_audits(compliance_page):
    """Pre-populate the 20 real audit/certification records for the compliance page."""
    for record in AUDIT_RECORDS:
        AuditStatus.objects.create(page=compliance_page, **record)
    logger.info("   ↳ Seeded %d audit status records.", len(AUDIT_RECORDS))


class Seeder:
    """Base seeder class."""

    def __init__(self, clean=False):
        self.clean = clean

    def run(self):
        raise NotImplementedError

    def clean_data(self):
        """Delete existing data before seeding."""
        raise NotImplementedError


class HomeSeeder(Seeder):
    def clean_data(self):
        # Clean section models first
        HomeHeroSectionFactory._meta.model.objects.all().delete()
        HomeIntroductionSectionFactory._meta.model.objects.all().delete()
        HomeServicesSectionFactory._meta.model.objects.all().delete()
        HomeStatsSectionFactory._meta.model.objects.all().delete()

        # Then clean content models
        HomeCarouselSlideFactory._meta.model.objects.all().delete()
        HomeIntroductionFeatureFactory._meta.model.objects.all().delete()
        CompanyStatsFactory._meta.model.objects.all().delete()
        ServiceFactory._meta.model.objects.all().delete()

        logger.info("🧹 Home data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Home data...")

        # Create sections first
        hero_section = HomeHeroSectionFactory.create()
        intro_section = HomeIntroductionSectionFactory.create()
        services_section = HomeServicesSectionFactory.create()
        stats_section = HomeStatsSectionFactory.create()

        # Then create content items that reference the sections
        HomeCarouselSlideFactory.create_batch(3, section=hero_section)
        HomeIntroductionFeatureFactory.create_batch(3, introduction=intro_section)
        ServiceFactory.create_batch(3, section=services_section)
        CompanyStatsFactory.create_batch(4, section=stats_section)

        # Create the sample activities with featured flag for the home page
        for sample in SAMPLE_ACTIVITIES:
            ActivityFactory.create(is_featured=True, **sample)

        # Create customers with featured flag for home page
        CustomerFactory.create_batch(4, is_featured=True)

        logger.info("✅ Home data seeded.")


class AboutSeeder(Seeder):
    def clean_data(self):
        # Clean section models first
        AboutSectionFactory._meta.model.objects.all().delete()
        TeamSectionFactory._meta.model.objects.all().delete()
        FAQSectionFactory._meta.model.objects.all().delete()

        # Then clean content models
        TeamMemberFactory._meta.model.objects.all().delete()
        FAQFactory._meta.model.objects.all().delete()

        logger.info("🧹 About data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding About data...")

        # Create sections first
        AboutSectionFactory.create()
        team_section = TeamSectionFactory.create()
        faq_section = FAQSectionFactory.create()

        # Then create content items
        TeamMemberFactory.create_batch(5, section=team_section, is_management=True)
        TeamMemberFactory.create_batch(10, section=team_section, is_management=False)
        FAQFactory.create_batch(5, section=faq_section)

        logger.info("✅ About data seeded.")


class CustomerSeeder(Seeder):
    def clean_data(self):
        # Clean section models first
        CustomersSectionFactory._meta.model.objects.all().delete()
        TestimonialsSectionFactory._meta.model.objects.all().delete()

        # Then clean content models
        CustomerFactory._meta.model.objects.all().delete()
        TestimonialFactory._meta.model.objects.all().delete()

        logger.info("🧹 Customer data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Customer data...")

        # Create sections first
        customers_section = CustomersSectionFactory.create()
        testimonials_section = TestimonialsSectionFactory.create()

        # Then create content items
        CustomerFactory.create_batch(10, section=customers_section)
        TestimonialFactory.create_batch(4, section=testimonials_section)
        # Set one testimonial as featured
        TestimonialFactory.create(section=testimonials_section, is_featured=True)

        logger.info("✅ Customer data seeded.")


class ContactSeeder(Seeder):
    def clean_data(self):
        # Clean section model first
        ContactSectionFactory._meta.model.objects.all().delete()

        # Then clean content models
        ContactDataFactory._meta.model.objects.all().delete()
        ContactGroupFactory._meta.model.objects.all().delete()
        ContactMemberFactory._meta.model.objects.all().delete()
        SocialFactory._meta.model.objects.all().delete()
        ContactPhoneFactory._meta.model.objects.all().delete()
        ContactEmailFactory._meta.model.objects.all().delete()

        logger.info("🧹 Contact data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Contact data...")

        # Create section first
        contact_section = ContactSectionFactory.create()

        # Create contact data
        contact_data = ContactDataFactory.create(section=contact_section)

        # Add phone numbers and emails
        ContactPhoneFactory.create(contact=contact_data, type="phone", is_primary=True)
        ContactPhoneFactory.create(contact=contact_data, type="whatsapp")

        ContactEmailFactory.create(
            contact=contact_data, department="Sales", is_primary=True
        )
        ContactEmailFactory.create(contact=contact_data, department="Support")

        # Create groups and members
        for dept in ["Sales", "Production"]:
            group = ContactGroupFactory.create(section=contact_section, name=dept)
            ContactMemberFactory.create_batch(3, group=group)

        # Create social media links
        SocialFactory.create_batch(3, section=contact_section)

        logger.info("✅ Contact data seeded.")


class CareerSeeder(Seeder):
    def clean_data(self):
        # Clean section model first
        CareerSectionFactory._meta.model.objects.all().delete()

        # Then clean content models (applications cascade with their position,
        # but clear explicitly so re-seeds start from a clean slate)
        JobApplicationFactory._meta.model.objects.all().delete()
        CareerPositionFactory._meta.model.objects.all().delete()

        logger.info("🧹 Career data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Career data...")

        # Create section first
        career_section = CareerSectionFactory.create()

        # Then create positions
        positions = CareerPositionFactory.create_batch(
            3, section=career_section, status="active"
        )

        # A few sample applications per position for testing the apply flow/admin
        for position in positions:
            JobApplicationFactory.create_batch(2, position=position)

        logger.info("✅ Career data seeded.")


class ActivitiesSeeder(Seeder):
    def clean_data(self):
        # Clean section model first
        ActivitiesSectionFactory._meta.model.objects.all().delete()

        # Then clean content models
        ActivityFactory._meta.model.objects.all().delete()

        logger.info("🧹 Activities data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Activities data...")

        # Create section first
        activities_section = ActivitiesSectionFactory.create()

        # Then create the sample activities, featured so they show on the home page
        for sample in SAMPLE_ACTIVITIES:
            ActivityFactory.create(
                section=activities_section, is_featured=True, **sample
            )

        logger.info("✅ Activities data seeded.")


class ProductsSeeder(Seeder):
    def clean_data(self):
        # Clean section models first
        ProductsPageFactory._meta.model.objects.all().delete()

        # Then clean content models
        ProductCarouselSlideFactory._meta.model.objects.all().delete()
        ProductSectionFactory._meta.model.objects.all().delete()
        ProductCategoryFactory._meta.model.objects.all().delete()
        ProductFactory._meta.model.objects.all().delete()

        logger.info("🧹 Products data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Products data...")

        # Create main page
        products_page = ProductsPageFactory.create()

        # Create carousel slides
        ProductCarouselSlideFactory.create_batch(3, page=products_page)

        # Create sections (some before, some after products)
        ProductSectionFactory.create_batch(3, page=products_page, after_products=False)
        ProductSectionFactory.create_batch(2, page=products_page, after_products=True)

        # Create product categories and products
        for category_name in ["Jackets", "Pants", "Shirts", "Denim"]:
            category = ProductCategoryFactory.create(
                page=products_page, name=category_name
            )
            # Create 5-10 products for each category
            product_count = random.randint(5, 10)
            ProductFactory.create_batch(product_count, category=category)

        logger.info("✅ Products data seeded.")


class ComplianceSeeder(Seeder):
    def clean_data(self):
        # Clean section models first
        CompliancePageFactory._meta.model.objects.all().delete()

        # Then clean content models
        ComplianceSectionFactory._meta.model.objects.all().delete()
        ComplianceCertificateFactory._meta.model.objects.all().delete()
        AuditStatus.objects.all().delete()

        logger.info("🧹 Compliance data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Compliance data...")

        # Create main page
        compliance_page = CompliancePageFactory.create()

        # Create content sections
        ComplianceSectionFactory.create_batch(5, page=compliance_page)

        # Create certificates
        ComplianceCertificateFactory.create_batch(7, page=compliance_page)

        # Pre-populate the real audit status records
        seed_audits(compliance_page)

        logger.info("✅ Compliance data seeded.")


class SustainabilitySeeder(Seeder):
    def clean_data(self):
        # Clean section models first
        SustainabilityPageFactory._meta.model.objects.all().delete()

        # Then clean content models
        SustainabilitySectionFactory._meta.model.objects.all().delete()
        SustainabilityCertificateFactory._meta.model.objects.all().delete()

        logger.info("🧹 Sustainability data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Sustainability data...")

        # Create main page
        sustainability_page = SustainabilityPageFactory.create()

        # Create content sections
        SustainabilitySectionFactory.create_batch(5, page=sustainability_page)

        # Create certificates
        SustainabilityCertificateFactory.create_batch(5, page=sustainability_page)

        logger.info("✅ Sustainability data seeded.")


class GallerySeeder(Seeder):
    def clean_data(self):
        # Clean section models first
        GalleryPageFactory._meta.model.objects.all().delete()

        # Then clean content models
        GallerySectionFactory._meta.model.objects.all().delete()
        GalleryImageFactory._meta.model.objects.all().delete()
        GalleryVideoFactory._meta.model.objects.all().delete()

        logger.info("🧹 Gallery data cleaned.")

    @transaction.atomic
    def run(self):
        if self.clean:
            self.clean_data()
        logger.info("🌱 Seeding Gallery data...")

        # Create main page
        gallery_page = GalleryPageFactory.create()

        # Create gallery sections
        sections = ["Products", "Factory", "Team", "Events"]
        for section_name in sections:
            section = GallerySectionFactory.create(page=gallery_page, name=section_name)

            # Create images for each section
            GalleryImageFactory.create_batch(8, section=section)

            # Create videos for each section (fewer videos than images)
            GalleryVideoFactory.create_batch(2, section=section)

        logger.info("✅ Gallery data seeded.")
