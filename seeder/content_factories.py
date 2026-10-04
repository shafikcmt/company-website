"""factory_boy factories with realistic garment-industry defaults.

The seeders in content_seeder.py pass explicit values from seeder/data.py;
the defaults here keep ad-hoc `XFactory.create()` calls (tests, shell)
meaningful instead of lorem ipsum.
"""

import factory
from faker import Faker

from seeder import data
from seeder.utils import cache_image
from hapl.models import (
    SiteSettings,
    NavbarSettings,
    HomeHeroSection,
    HomeIntroductionSection,
    HomeServicesSection,
    HomeStatsSection,
    AboutSection,
    WhyUsSection,
    WhyUsFeature,
    TeamSection,
    FAQSection,
    CustomersSection,
    TestimonialsSection,
    ContactSection,
    CareerSection,
    ActivitiesSection,
    HomeCarouselSlide,
    HomeIntroductionFeature,
    Service,
    CompanyStats,
    TeamMember,
    FAQ,
    Customer,
    Testimonial,
    ContactData,
    ContactPhone,
    ContactEmail,
    ContactGroup,
    ContactMember,
    Social,
    CareerPosition,
    JobApplication,
    Activity,
    ProductsPage,
    ProductCarouselSlide,
    ProductSection,
    ProductCategory,
    Product,
    CompliancePage,
    ComplianceSection,
    ComplianceCertificate,
    SustainabilityPage,
    SustainabilitySection,
    SustainabilityCertificate,
    GalleryPage,
    GallerySection,
    GalleryImage,
    GalleryVideo,
)


fake = Faker()


def image(width, height, keyword, label=None, style="photo"):
    return factory.LazyFunction(
        lambda: cache_image(width, height, keyword=keyword, label=label or keyword, style=style)
    )


def iterate(items, key):
    return factory.Iterator([item[key] for item in items])


class BaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True


# --- Settings ---------------------------------------------------------------
class SiteSettingsFactory(BaseFactory):
    class Meta:
        model = SiteSettings
        django_get_or_create = ("id",)

    id = 1
    site_name = data.SITE["site_name"]
    site_tagline = data.SITE["site_tagline"]


class NavbarSettingsFactory(BaseFactory):
    class Meta:
        model = NavbarSettings
        django_get_or_create = ("id",)

    id = 1


# --- Sections / pages -------------------------------------------------------
class HomeHeroSectionFactory(BaseFactory):
    class Meta:
        model = HomeHeroSection

    badge_text = data.HERO["badge_text"]
    title = data.HERO["title"]
    highlight_word = data.HERO["highlight_word"]
    subtitle = data.HERO["subtitle"]
    cta_primary_text = data.HERO["cta_primary_text"]
    cta_primary_url = data.HERO["cta_primary_url"]
    cta_secondary_text = data.HERO["cta_secondary_text"]
    cta_secondary_url = data.HERO["cta_secondary_url"]
    bottom_label = data.HERO["bottom_label"]
    bottom_link_text = data.HERO["bottom_link_text"]
    bottom_link_url = data.HERO["bottom_link_url"]
    autoplay = True
    autoplay_interval = 6
    is_active = True


class HomeIntroductionSectionFactory(BaseFactory):
    class Meta:
        model = HomeIntroductionSection

    eyebrow = data.INTRO["eyebrow"]
    title = data.INTRO["title"]
    subtitle = data.INTRO["subtitle"]
    content = data.INTRO["content"]
    cta_text = data.INTRO["cta_text"]
    cta_url = data.INTRO["cta_url"]
    image = image(1600, 1200, "factory", "Humana Apparels factory")


class HomeServicesSectionFactory(BaseFactory):
    class Meta:
        model = HomeServicesSection

    eyebrow = data.SERVICES_SECTION["eyebrow"]
    title = data.SERVICES_SECTION["title"]
    subtitle = data.SERVICES_SECTION["subtitle"]


class HomeStatsSectionFactory(BaseFactory):
    class Meta:
        model = HomeStatsSection

    title = data.STATS_SECTION["title"]
    subtitle = data.STATS_SECTION["subtitle"]


class AboutSectionFactory(BaseFactory):
    class Meta:
        model = AboutSection

    eyebrow = data.ABOUT["eyebrow"]
    title = data.ABOUT["title"]
    subtitle = data.ABOUT["subtitle"]
    content = data.ABOUT["content"]
    banner_title = data.ABOUT["banner_title"]
    banner_subtitle = data.ABOUT["banner_subtitle"]
    image = image(1600, 1200, "about", "Our factory in Gorai, Mirzapur")


class WhyUsSectionFactory(BaseFactory):
    class Meta:
        model = WhyUsSection

    eyebrow = data.CORE_VALUES_SECTION["eyebrow"]
    title = data.CORE_VALUES_SECTION["title"]
    subtitle = data.CORE_VALUES_SECTION["subtitle"]


class TeamSectionFactory(BaseFactory):
    class Meta:
        model = TeamSection

    eyebrow = data.TEAM_SECTION["eyebrow"]
    title = data.TEAM_SECTION["title"]
    subtitle = data.TEAM_SECTION["subtitle"]


class FAQSectionFactory(BaseFactory):
    class Meta:
        model = FAQSection

    eyebrow = data.FAQ_SECTION["eyebrow"]
    title = data.FAQ_SECTION["title"]
    subtitle = data.FAQ_SECTION["subtitle"]


class CustomersSectionFactory(BaseFactory):
    class Meta:
        model = CustomersSection

    eyebrow = data.CUSTOMERS_PAGE["eyebrow"]
    title = data.CUSTOMERS_PAGE["title"]
    subtitle = data.CUSTOMERS_PAGE["subtitle"]
    banner_title = data.CUSTOMERS_PAGE["banner_title"]
    banner_subtitle = data.CUSTOMERS_PAGE["banner_subtitle"]


class TestimonialsSectionFactory(BaseFactory):
    class Meta:
        model = TestimonialsSection

    eyebrow = data.TESTIMONIALS_SECTION["eyebrow"]
    title = data.TESTIMONIALS_SECTION["title"]
    subtitle = data.TESTIMONIALS_SECTION["subtitle"]


class ContactSectionFactory(BaseFactory):
    class Meta:
        model = ContactSection

    eyebrow = data.CONTACT_PAGE["eyebrow"]
    title = data.CONTACT_PAGE["title"]
    subtitle = data.CONTACT_PAGE["subtitle"]
    banner_title = data.CONTACT_PAGE["banner_title"]
    banner_subtitle = data.CONTACT_PAGE["banner_subtitle"]
    groups_title = data.CONTACT_PAGE["groups_title"]
    groups_empty_text = data.CONTACT_PAGE["groups_empty_text"]
    socials_title = data.CONTACT_PAGE["socials_title"]


class CareerSectionFactory(BaseFactory):
    class Meta:
        model = CareerSection

    eyebrow = data.CAREER_PAGE["eyebrow"]
    title = data.CAREER_PAGE["title"]
    subtitle = data.CAREER_PAGE["subtitle"]
    banner_title = data.CAREER_PAGE["banner_title"]
    banner_subtitle = data.CAREER_PAGE["banner_subtitle"]
    positions_title = data.CAREER_PAGE["positions_title"]
    positions_empty_text = data.CAREER_PAGE["positions_empty_text"]


class ActivitiesSectionFactory(BaseFactory):
    class Meta:
        model = ActivitiesSection

    eyebrow = data.ACTIVITIES_PAGE["eyebrow"]
    title = data.ACTIVITIES_PAGE["title"]
    subtitle = data.ACTIVITIES_PAGE["subtitle"]
    banner_title = data.ACTIVITIES_PAGE["banner_title"]
    banner_subtitle = data.ACTIVITIES_PAGE["banner_subtitle"]


class ProductsPageFactory(BaseFactory):
    class Meta:
        model = ProductsPage

    eyebrow = data.PRODUCTS_PAGE["eyebrow"]
    title = data.PRODUCTS_PAGE["title"]
    subtitle = data.PRODUCTS_PAGE["subtitle"]
    banner_title = data.PRODUCTS_PAGE["banner_title"]
    banner_subtitle = data.PRODUCTS_PAGE["banner_subtitle"]
    portfolio_eyebrow = data.PRODUCTS_PAGE["portfolio_eyebrow"]
    portfolio_title = data.PRODUCTS_PAGE["portfolio_title"]
    portfolio_subtitle = data.PRODUCTS_PAGE["portfolio_subtitle"]
    cta_title = data.PRODUCTS_PAGE["cta_title"]
    cta_text = data.PRODUCTS_PAGE["cta_text"]
    cta_button_text = data.PRODUCTS_PAGE["cta_button_text"]
    cta_button_url = data.PRODUCTS_PAGE["cta_button_url"]


class CompliancePageFactory(BaseFactory):
    class Meta:
        model = CompliancePage

    eyebrow = data.COMPLIANCE_PAGE["eyebrow"]
    title = data.COMPLIANCE_PAGE["title"]
    subtitle = data.COMPLIANCE_PAGE["subtitle"]
    banner_title = data.COMPLIANCE_PAGE["banner_title"]
    banner_subtitle = data.COMPLIANCE_PAGE["banner_subtitle"]
    audit_eyebrow = data.COMPLIANCE_PAGE["audit_eyebrow"]
    audit_title = data.COMPLIANCE_PAGE["audit_title"]
    audit_description = data.COMPLIANCE_PAGE["audit_description"]
    standards_title = data.COMPLIANCE_PAGE["standards_title"]
    standards_description = data.COMPLIANCE_PAGE["standards_description"]
    certificates_eyebrow = data.COMPLIANCE_PAGE["certificates_eyebrow"]
    certificates_title = data.COMPLIANCE_PAGE["certificates_title"]
    cta_title = data.COMPLIANCE_PAGE["cta_title"]
    cta_text = data.COMPLIANCE_PAGE["cta_text"]
    cta_button_text = data.COMPLIANCE_PAGE["cta_button_text"]
    cta_button_url = data.COMPLIANCE_PAGE["cta_button_url"]


class SustainabilityPageFactory(BaseFactory):
    class Meta:
        model = SustainabilityPage

    eyebrow = data.SUSTAINABILITY_PAGE["eyebrow"]
    title = data.SUSTAINABILITY_PAGE["title"]
    subtitle = data.SUSTAINABILITY_PAGE["subtitle"]
    banner_title = data.SUSTAINABILITY_PAGE["banner_title"]
    banner_subtitle = data.SUSTAINABILITY_PAGE["banner_subtitle"]
    certificates_title = data.SUSTAINABILITY_PAGE["certificates_title"]
    cta_title = data.SUSTAINABILITY_PAGE["cta_title"]
    cta_text = data.SUSTAINABILITY_PAGE["cta_text"]
    cta_button_text = data.SUSTAINABILITY_PAGE["cta_button_text"]
    cta_button_url = data.SUSTAINABILITY_PAGE["cta_button_url"]


class GalleryPageFactory(BaseFactory):
    class Meta:
        model = GalleryPage

    eyebrow = data.GALLERY_PAGE["eyebrow"]
    title = data.GALLERY_PAGE["title"]
    subtitle = data.GALLERY_PAGE["subtitle"]
    banner_title = data.GALLERY_PAGE["banner_title"]
    banner_subtitle = data.GALLERY_PAGE["banner_subtitle"]
    all_tab_label = data.GALLERY_PAGE["all_tab_label"]
    videos_title = data.GALLERY_PAGE["videos_title"]


# --- Content ----------------------------------------------------------------
class HomeCarouselSlideFactory(BaseFactory):
    class Meta:
        model = HomeCarouselSlide

    section = factory.SubFactory(HomeHeroSectionFactory)
    alt_text = iterate(data.HERO_SLIDES, "alt_text")
    caption = iterate(data.HERO_SLIDES, "caption")
    focal_point = iterate(data.HERO_SLIDES, "focal_point")
    image = factory.LazyAttribute(lambda o: cache_image(2400, 1600, keyword=f"hero-{o.order}", label=o.caption))
    is_active = True
    order = factory.Sequence(lambda n: n)


class HomeIntroductionFeatureFactory(BaseFactory):
    class Meta:
        model = HomeIntroductionFeature

    introduction = factory.SubFactory(HomeIntroductionSectionFactory)
    icon = iterate(data.INTRO_FEATURES, "icon")
    title = iterate(data.INTRO_FEATURES, "title")
    description = iterate(data.INTRO_FEATURES, "description")


class ServiceFactory(BaseFactory):
    class Meta:
        model = Service

    section = factory.SubFactory(HomeServicesSectionFactory)
    title = iterate(data.SERVICES, "title")
    description = iterate(data.SERVICES, "description")
    icon = iterate(data.SERVICES, "icon")
    image = factory.LazyAttribute(lambda o: cache_image(800, 500, keyword=f"service-{o.order}", label=o.title))
    order = factory.Sequence(lambda n: n)


class CompanyStatsFactory(BaseFactory):
    class Meta:
        model = CompanyStats

    section = factory.SubFactory(HomeStatsSectionFactory)
    icon = iterate(data.STATS, "icon")
    number = iterate(data.STATS, "number")
    suffix = iterate(data.STATS, "suffix")
    label = iterate(data.STATS, "label")
    order = factory.Sequence(lambda n: n)


class WhyUsFeatureFactory(BaseFactory):
    class Meta:
        model = WhyUsFeature

    section = factory.SubFactory(WhyUsSectionFactory)
    icon = iterate(data.CORE_VALUES, "icon")
    title = iterate(data.CORE_VALUES, "title")
    description = iterate(data.CORE_VALUES, "description")
    order = factory.Sequence(lambda n: n)


class TeamMemberFactory(BaseFactory):
    class Meta:
        model = TeamMember

    section = factory.SubFactory(TeamSectionFactory)
    name = iterate(data.MANAGEMENT + data.STAFF, "name")
    position = iterate(data.MANAGEMENT + data.STAFF, "position")
    image = factory.LazyAttribute(lambda o: cache_image(600, 800, keyword=f"person-{o.name}", label=o.name))
    is_management = False
    linkedin_url = None
    order = factory.Sequence(lambda n: n)


class FAQFactory(BaseFactory):
    class Meta:
        model = FAQ

    section = factory.SubFactory(FAQSectionFactory)
    question = iterate(data.FAQS, "question")
    answer = iterate(data.FAQS, "answer")
    order = factory.Sequence(lambda n: n)


class CustomerFactory(BaseFactory):
    class Meta:
        model = Customer

    section = factory.SubFactory(CustomersSectionFactory)
    name = iterate(data.CUSTOMERS, "name")
    url = iterate(data.CUSTOMERS, "url")
    logo = factory.LazyAttribute(lambda o: cache_image(400, 200, keyword=f"logo-{o.name}", label=o.name, style="logo"))
    is_featured = iterate(data.CUSTOMERS, "is_featured")
    order = factory.Sequence(lambda n: n)


class TestimonialFactory(BaseFactory):
    class Meta:
        model = Testimonial

    section = factory.SubFactory(TestimonialsSectionFactory)
    content = iterate(data.TESTIMONIALS, "content")
    author = iterate(data.TESTIMONIALS, "author")
    position = iterate(data.TESTIMONIALS, "position")
    company_logo = factory.LazyAttribute(
        lambda o: cache_image(200, 200, keyword=f"brand-{o.position}", label=o.position.split(", ")[-1], style="logo")
    )
    is_featured = iterate(data.TESTIMONIALS, "is_featured")
    order = factory.Sequence(lambda n: n)


class ContactDataFactory(BaseFactory):
    class Meta:
        model = ContactData

    section = factory.SubFactory(ContactSectionFactory)
    office_title = data.CONTACT_DATA["office_title"]
    office_subtitle = data.CONTACT_DATA["office_subtitle"]
    address = data.CONTACT_DATA["address"]
    fax = data.CONTACT_DATA["fax"]
    map_title = data.CONTACT_DATA["map_title"]
    map_subtitle = data.CONTACT_DATA["map_subtitle"]
    map_url = data.CONTACT_DATA["map_url"]
    map_image = image(1600, 1000, "map", "Gorai, Mirzapur")
    office_image = image(1600, 1000, "office", "Factory & office")


class ContactPhoneFactory(BaseFactory):
    class Meta:
        model = ContactPhone

    contact = factory.SubFactory(ContactDataFactory)
    number = iterate(data.CONTACT_PHONES, "number")
    type = iterate(data.CONTACT_PHONES, "type")
    is_primary = iterate(data.CONTACT_PHONES, "is_primary")


class ContactEmailFactory(BaseFactory):
    class Meta:
        model = ContactEmail

    contact = factory.SubFactory(ContactDataFactory)
    email = iterate(data.CONTACT_EMAILS, "email")
    department = iterate(data.CONTACT_EMAILS, "department")
    is_primary = iterate(data.CONTACT_EMAILS, "is_primary")


class ContactGroupFactory(BaseFactory):
    class Meta:
        model = ContactGroup

    section = factory.SubFactory(ContactSectionFactory)
    name = factory.Iterator(list(data.CONTACT_GROUPS))


class ContactMemberFactory(BaseFactory):
    class Meta:
        model = ContactMember

    group = factory.SubFactory(ContactGroupFactory)
    name = "Mahmudul Hasan"
    position = "Senior Merchandiser"
    email = "merchandising@humanaapparels.com"
    phone = "+8801711002002"
    image = factory.LazyAttribute(lambda o: cache_image(400, 400, keyword=f"person-{o.name}", label=o.name))


class SocialFactory(BaseFactory):
    class Meta:
        model = Social

    section = factory.SubFactory(ContactSectionFactory)
    name = iterate(data.SOCIALS, "name")
    url = iterate(data.SOCIALS, "url")
    icon = iterate(data.SOCIALS, "icon")
    order = factory.Sequence(lambda n: n)


class CareerPositionFactory(BaseFactory):
    class Meta:
        model = CareerPosition

    section = factory.SubFactory(CareerSectionFactory)
    title = iterate(data.POSITIONS, "title")
    department = iterate(data.POSITIONS, "department")
    location = iterate(data.POSITIONS, "location")
    type = iterate(data.POSITIONS, "type")
    job_type = iterate(data.POSITIONS, "job_type")
    description = iterate(data.POSITIONS, "description")
    posted_at = factory.Faker("date_between", start_date="-30d", end_date="today")
    deadline = factory.Faker("date_between", start_date="+14d", end_date="+45d")
    apply_email = "careers@humanaapparels.com"
    status = "active"
    order = factory.Sequence(lambda n: n)


class JobApplicationFactory(BaseFactory):
    class Meta:
        model = JobApplication

    position = factory.SubFactory(CareerPositionFactory)
    full_name = factory.Iterator(["Rakib Hasan", "Moushumi Akter", "Sajid Karim", "Nadia Islam", "Fahim Reza", "Tania Sultana"])
    email = factory.LazyAttribute(lambda o: f"{o.full_name.split()[0].lower()}.{fake.random_int(10, 99)}@example.com")
    phone = factory.LazyFunction(lambda: fake.numerify("+88017########"))
    experience_years = factory.Faker("pydecimal", right_digits=1, min_value=1, max_value=12)
    cover_letter = (
        "I have several years of experience in woven garment production and would "
        "welcome the chance to contribute to your team."
    )
    # A small valid PDF so the resume passes the model's extension/size validators.
    resume = factory.django.FileField(filename="resume.pdf", data=b"%PDF-1.4 sample resume for testing")
    status = factory.Iterator(["new", "reviewed", "shortlisted"])


class ActivityFactory(BaseFactory):
    class Meta:
        model = Activity

    section = factory.SubFactory(ActivitiesSectionFactory)
    title = iterate(data.ACTIVITIES, "title")
    excerpt = iterate(data.ACTIVITIES, "excerpt")
    tag = iterate(data.ACTIVITIES, "tag")
    activity_date = iterate(data.ACTIVITIES, "activity_date")
    is_featured = iterate(data.ACTIVITIES, "is_featured")
    content = None
    image = factory.LazyAttribute(lambda o: cache_image(1600, 1000, keyword=f"activity-{o.title}", label=o.tag))


class ProductCarouselSlideFactory(BaseFactory):
    class Meta:
        model = ProductCarouselSlide

    page = factory.SubFactory(ProductsPageFactory)
    alt = factory.Iterator(data.PRODUCT_CAROUSEL)
    image = factory.LazyAttribute(lambda o: cache_image(2400, 1200, keyword=f"products-{o.alt}", label=o.alt))
    order = factory.Sequence(lambda n: n)


class ProductSectionFactory(BaseFactory):
    class Meta:
        model = ProductSection

    page = factory.SubFactory(ProductsPageFactory)
    eyebrow = iterate(data.PRODUCT_SECTIONS, "eyebrow")
    title = iterate(data.PRODUCT_SECTIONS, "title")
    description = iterate(data.PRODUCT_SECTIONS, "description")
    after_products = iterate(data.PRODUCT_SECTIONS, "after_products")
    image = factory.LazyAttribute(lambda o: cache_image(1600, 1200, keyword=f"psection-{o.title}", label=o.title))
    order = factory.Sequence(lambda n: n)


class ProductCategoryFactory(BaseFactory):
    class Meta:
        model = ProductCategory

    page = factory.SubFactory(ProductsPageFactory)
    name = factory.Iterator(list(data.PRODUCT_CATEGORIES))
    order = factory.Sequence(lambda n: n)


class ProductFactory(BaseFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(ProductCategoryFactory)
    name = "Men's Hooded Down Jacket"
    gender = "Male"
    buyer = "Hugo Boss"
    image = factory.LazyAttribute(lambda o: cache_image(800, 800, keyword=f"product-{o.name}", label=o.name))
    order = factory.Sequence(lambda n: n)


class ComplianceSectionFactory(BaseFactory):
    class Meta:
        model = ComplianceSection

    page = factory.SubFactory(CompliancePageFactory)
    eyebrow = iterate(data.COMPLIANCE_SECTIONS, "eyebrow")
    title = iterate(data.COMPLIANCE_SECTIONS, "title")
    description = iterate(data.COMPLIANCE_SECTIONS, "description")
    image = factory.LazyAttribute(lambda o: cache_image(1600, 1000, keyword=f"compliance-{o.title}", label=o.eyebrow))
    order = factory.Sequence(lambda n: n)


class ComplianceCertificateFactory(BaseFactory):
    class Meta:
        model = ComplianceCertificate

    page = factory.SubFactory(CompliancePageFactory)
    name = factory.Iterator([name for name, _ in data.COMPLIANCE_CERTIFICATES])
    website_url = factory.Iterator([url for _, url in data.COMPLIANCE_CERTIFICATES])
    image = factory.LazyAttribute(lambda o: cache_image(400, 400, keyword=f"cert-{o.name}", label=o.name, style="logo"))
    is_active = True
    order = factory.Sequence(lambda n: n)


class SustainabilitySectionFactory(BaseFactory):
    class Meta:
        model = SustainabilitySection

    page = factory.SubFactory(SustainabilityPageFactory)
    title = iterate(data.SUSTAINABILITY_SECTIONS, "title")
    description = iterate(data.SUSTAINABILITY_SECTIONS, "description")
    image = factory.LazyAttribute(lambda o: cache_image(1200, 1200, keyword=f"sustain-{o.title}", label=o.title))
    order = factory.Sequence(lambda n: n)


class SustainabilityCertificateFactory(BaseFactory):
    class Meta:
        model = SustainabilityCertificate

    page = factory.SubFactory(SustainabilityPageFactory)
    name = factory.Iterator(data.SUSTAINABILITY_CERTIFICATES)
    image = factory.LazyAttribute(lambda o: cache_image(400, 400, keyword=f"cert-{o.name}", label=o.name, style="logo"))
    order = factory.Sequence(lambda n: n)


class GallerySectionFactory(BaseFactory):
    class Meta:
        model = GallerySection

    page = factory.SubFactory(GalleryPageFactory)
    name = factory.Iterator(list(data.GALLERY_SECTIONS))
    order = factory.Sequence(lambda n: n)


class GalleryImageFactory(BaseFactory):
    class Meta:
        model = GalleryImage

    section = factory.SubFactory(GallerySectionFactory)
    caption = "Sewing line"
    image = factory.LazyAttribute(lambda o: cache_image(1600, 1200, keyword=f"gallery-{o.caption}", label=o.caption))
    order = factory.Sequence(lambda n: n)


class GalleryVideoFactory(BaseFactory):
    """Not used by the default seed (no verified company videos to embed)."""

    class Meta:
        model = GalleryVideo

    section = factory.SubFactory(GallerySectionFactory)
    caption = "Factory walkthrough"
    youtube_url = "https://www.youtube.com/embed/"
    order = 0
