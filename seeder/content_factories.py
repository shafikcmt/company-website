import factory
from faker import Faker
from seeder.utils import cache_image
from hapl.models import (
    HomeHeroSection,
    HomeIntroductionSection,
    HomeServicesSection,
    HomeStatsSection,
    AboutSection,
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


class BaseFactory(factory.django.DjangoModelFactory):
    """Abstract base factory with common settings."""

    class Meta:
        abstract = True


# --- Section Factories ---


class BaseSectionFactory(BaseFactory):
    """Base factory for section models"""

    title = factory.Faker("sentence", nb_words=5)
    subtitle = factory.Faker("sentence", nb_words=12)

    class Meta:
        abstract = True


class HomeHeroSectionFactory(BaseFactory):
    class Meta:
        model = HomeHeroSection

    badge_text = "Bangladesh's Premier Garment Manufacturer"
    title = "Quality Apparel, Crafted Responsibly"
    subtitle = "Delivering compliant, sustainable garments to global brands."
    cta_primary_text = "Explore Products"
    cta_primary_url = "/products/"
    cta_primary_active = True
    cta_secondary_text = "Contact Us"
    cta_secondary_url = "/contact/"
    cta_secondary_active = True


class HomeIntroductionSectionFactory(BaseSectionFactory):
    class Meta:
        model = HomeIntroductionSection

    title = "Crafting Excellence in Apparel Manufacturing"
    subtitle = "We combine traditional craftsmanship with modern technology that meet global standards."
    content = factory.Faker("paragraph", nb_sentences=5)
    image = factory.LazyAttribute(lambda x: cache_image(1920, 1080, keyword="factory"))


class HomeServicesSectionFactory(BaseSectionFactory):
    class Meta:
        model = HomeServicesSection

    title = "Our Services"
    subtitle = "Comprehensive apparel manufacturing solutions tailored to your needs"


class HomeStatsSectionFactory(BaseSectionFactory):
    class Meta:
        model = HomeStatsSection

    title = "Our Impact in Numbers"
    subtitle = "Key metrics that showcase our growth and success"


class AboutSectionFactory(BaseSectionFactory):
    class Meta:
        model = AboutSection

    title = "Our Story"
    subtitle = "From humble beginnings to a global apparel manufacturing leader."
    content = factory.Faker("paragraph", nb_sentences=8)
    image = factory.LazyAttribute(lambda x: cache_image(1920, 1080, keyword="factory"))


class TeamSectionFactory(BaseSectionFactory):
    class Meta:
        model = TeamSection

    title = "Our Team"
    subtitle = "Meet the experts behind our success"


class FAQSectionFactory(BaseSectionFactory):
    class Meta:
        model = FAQSection

    title = "Frequently Asked Questions"
    subtitle = "Get answers to common questions about our services"


class CustomersSectionFactory(BaseSectionFactory):
    class Meta:
        model = CustomersSection

    title = "Trusted by Global Fashion Brands"
    subtitle = "Partnering with industry leaders in sustainable fashion manufacturing"


class TestimonialsSectionFactory(BaseSectionFactory):
    class Meta:
        model = TestimonialsSection

    title = "What Our Clients Say"
    subtitle = "Read what our clients have to say about us"


class ContactSectionFactory(BaseSectionFactory):
    class Meta:
        model = ContactSection

    title = "Contact Us"
    subtitle = "Get in touch with our team"


class CareerSectionFactory(BaseSectionFactory):
    class Meta:
        model = CareerSection

    title = "Career Opportunities"
    subtitle = "Join our team and grow with us"


class ActivitiesSectionFactory(BaseSectionFactory):
    class Meta:
        model = ActivitiesSection

    title = "Our Activities"
    subtitle = "CSR, compliance and community initiatives from across Humana Apparels"


# --- Content Factories ---


class HomeCarouselSlideFactory(BaseFactory):
    class Meta:
        model = HomeCarouselSlide

    section = factory.SubFactory(HomeHeroSectionFactory)
    title = factory.Faker("sentence", nb_words=5)
    subtitle = factory.Faker("sentence", nb_words=12)
    image = factory.LazyAttribute(lambda x: cache_image(1920, 1080, keyword="apparel"))
    cta_text = factory.Faker("word")
    cta_url = factory.Faker("url")
    is_active = True


class HomeIntroductionFeatureFactory(BaseFactory):
    class Meta:
        model = HomeIntroductionFeature

    introduction = factory.SubFactory(HomeIntroductionSectionFactory)
    icon = factory.Faker(
        "random_element",
        elements=[
            "ph-check-circle",
            "ph-rocket",
            "ph-star",
        ],
    )
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=2)


class ServiceFactory(BaseFactory):
    class Meta:
        model = Service

    section = factory.SubFactory(HomeServicesSectionFactory)
    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("paragraph", nb_sentences=4)
    icon = factory.Faker(
        "random_element",
        elements=[
            "ph-pen-nib",
            "ph-factory",
            "ph-leaf",
            "ph-truck",
            "ph-gear",
        ],
    )
    image = factory.LazyAttribute(lambda x: cache_image(560, 720, keyword="factory"))


class CompanyStatsFactory(BaseFactory):
    class Meta:
        model = CompanyStats

    section = factory.SubFactory(HomeStatsSectionFactory)
    title = factory.Faker("word")
    value = factory.Faker("numerify", text="##+")
    icon = factory.Faker(
        "random_element",
        elements=[
            "ph-calendar",
            "ph-users",
            "ph-t-shirt",
            "ph-globe",
            "ph-factory",
        ],
    )


class TeamMemberFactory(BaseFactory):
    class Meta:
        model = TeamMember

    section = factory.SubFactory(TeamSectionFactory)
    name = factory.Faker("name")
    position = factory.Faker("job")
    image = factory.LazyAttribute(lambda x: cache_image(320, 320, keyword="person"))
    is_management = factory.Faker("boolean")


class FAQFactory(BaseFactory):
    class Meta:
        model = FAQ

    section = factory.SubFactory(FAQSectionFactory)
    question = factory.Faker("sentence", nb_words=8)
    answer = factory.Faker("paragraph", nb_sentences=4)


class CustomerFactory(BaseFactory):
    class Meta:
        model = Customer

    section = factory.SubFactory(CustomersSectionFactory)
    name = factory.Faker("company")
    logo = factory.LazyAttribute(lambda x: cache_image(300, 200, keyword="brand"))
    url = factory.Faker("url")
    is_featured = factory.Faker("boolean", chance_of_getting_true=75)


class TestimonialFactory(BaseFactory):
    class Meta:
        model = Testimonial

    section = factory.SubFactory(TestimonialsSectionFactory)
    content = factory.Faker("paragraph", nb_sentences=4)
    author = factory.Faker("name")
    position = factory.Faker("job")
    company_logo = factory.LazyAttribute(
        lambda x: cache_image(200, 200, keyword="logo")
    )
    is_featured = factory.Faker("boolean", chance_of_getting_true=50)


class ContactDataFactory(BaseFactory):
    class Meta:
        model = ContactData

    section = factory.SubFactory(ContactSectionFactory)
    map_title = "Visit Our Headquarters"
    map_subtitle = "Get directions to our main office and manufacturing facility."
    map_image = factory.LazyAttribute(lambda x: cache_image(600, 400, keyword="map"))
    map_url = "https://www.google.com/maps"
    address = factory.Faker("address")
    office_title = "Contact Us"
    office_subtitle = "Reach out to our team for inquiries and support."
    office_image = factory.LazyAttribute(
        lambda x: cache_image(600, 400, keyword="office")
    )
    # max_length=20 — keep it short (faker's phone_number can exceed 20 chars)
    fax = factory.LazyFunction(lambda: fake.numerify("+8802########"))


class ContactPhoneFactory(BaseFactory):
    class Meta:
        model = ContactPhone

    contact = factory.SubFactory(ContactDataFactory)
    # max_length=20 — faker's phone_number can exceed 20 chars
    number = factory.LazyFunction(lambda: fake.numerify("+8801#########"))
    type = factory.Faker("random_element", elements=["phone", "whatsapp"])
    is_primary = factory.Faker("boolean", chance_of_getting_true=25)


class ContactEmailFactory(BaseFactory):
    class Meta:
        model = ContactEmail

    contact = factory.SubFactory(ContactDataFactory)
    email = factory.Faker("email")
    department = factory.Faker("job")
    is_primary = factory.Faker("boolean", chance_of_getting_true=25)


class ContactGroupFactory(BaseFactory):
    class Meta:
        model = ContactGroup

    section = factory.SubFactory(ContactSectionFactory)
    name = factory.Faker("word")


class ContactMemberFactory(BaseFactory):
    class Meta:
        model = ContactMember

    group = factory.SubFactory(ContactGroupFactory)
    name = factory.Faker("name")
    position = factory.Faker("job")
    image = factory.LazyAttribute(lambda x: cache_image(320, 320, keyword="person"))
    email = factory.Faker("email")
    # max_length=20 — faker's phone_number can exceed 20 chars
    phone = factory.LazyFunction(lambda: fake.numerify("+8801#########"))


class SocialFactory(BaseFactory):
    class Meta:
        model = Social

    section = factory.SubFactory(ContactSectionFactory)
    name = factory.Faker("word")
    url = factory.Faker("url")
    icon = factory.Faker(
        "random_element",
        elements=[
            "ph-facebook-logo",
            "ph-instagram-logo",
            "ph-linkedin-logo",
            "ph-twitter-logo",
        ],
    )


class CareerPositionFactory(BaseFactory):
    class Meta:
        model = CareerPosition

    section = factory.SubFactory(CareerSectionFactory)
    title = factory.Faker("sentence", nb_words=6)
    type = factory.Faker(
        "random_element", elements=["Full-time", "Part-time", "Contract"]
    )
    location = factory.Faker("city")
    department = factory.Faker("word")
    posted_at = factory.Faker("date_object")
    description = factory.Faker("paragraph", nb_sentences=6)
    status = factory.Faker("random_element", elements=["active", "inactive"])


class JobApplicationFactory(BaseFactory):
    class Meta:
        model = JobApplication

    position = factory.SubFactory(CareerPositionFactory)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = factory.LazyFunction(lambda: fake.numerify("+8801#########"))
    experience_years = factory.Faker(
        "pydecimal", right_digits=1, min_value=0, max_value=30
    )
    cover_letter = factory.Faker("paragraph", nb_sentences=4)
    # A small valid PDF so the resume passes the model's extension/size validators
    # and is downloadable from the admin.
    resume = factory.django.FileField(
        filename="resume.pdf", data=b"%PDF-1.4 sample resume for testing"
    )
    status = factory.Faker(
        "random_element",
        elements=["new", "reviewed", "shortlisted", "rejected", "hired"],
    )


class ActivityFactory(BaseFactory):
    class Meta:
        model = Activity

    section = factory.SubFactory(ActivitiesSectionFactory)
    # title/excerpt/tag are supplied explicitly from SAMPLE_ACTIVITIES by the
    # seeders (see content_seeder.py) so demo data uses real activity content,
    # not invented Faker text. content stays None — there is no detail page.
    title = factory.Faker("sentence", nb_words=7)
    excerpt = factory.Faker("sentence", nb_words=16)
    content = None
    image = factory.LazyAttribute(lambda x: cache_image(800, 600, keyword="csr"))
    activity_date = factory.Faker("date_between", start_date="-1y", end_date="today")
    tag = factory.Faker("word")
    is_featured = factory.Faker("boolean", chance_of_getting_true=25)


class ProductsPageFactory(BaseSectionFactory):
    class Meta:
        model = ProductsPage

    title = "Our Products"
    subtitle = "Explore our diverse range of high-quality apparel products"


class CompliancePageFactory(BaseSectionFactory):
    class Meta:
        model = CompliancePage

    title = "Compliance"
    subtitle = "Our commitment to ethical and sustainable manufacturing practices"


class SustainabilityPageFactory(BaseSectionFactory):
    class Meta:
        model = SustainabilityPage

    title = "Sustainability"
    subtitle = "Our initiatives for a greener and more sustainable future"


class GalleryPageFactory(BaseSectionFactory):
    class Meta:
        model = GalleryPage

    title = "Gallery"
    subtitle = "Visual showcase of our facilities, products, and team"


# Add these content factories
class ProductCarouselSlideFactory(BaseFactory):
    class Meta:
        model = ProductCarouselSlide

    page = factory.SubFactory(ProductsPageFactory)
    image = factory.LazyAttribute(lambda x: cache_image(800, 600, keyword="fashion"))
    alt = factory.Faker("sentence", nb_words=4)


class ProductSectionFactory(BaseFactory):
    class Meta:
        model = ProductSection

    page = factory.SubFactory(ProductsPageFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=5)
    image = factory.LazyAttribute(lambda x: cache_image(600, 400, keyword="apparel"))
    after_products = factory.Faker("boolean", chance_of_getting_true=20)


class ProductCategoryFactory(BaseFactory):
    class Meta:
        model = ProductCategory

    page = factory.SubFactory(ProductsPageFactory)
    name = factory.Faker(
        "random_element", elements=["Jackets", "Pants", "Shirts", "Denim", "Activewear"]
    )


class ProductFactory(BaseFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(ProductCategoryFactory)
    gender = factory.Faker("random_element", elements=["Male", "Female"])
    name = factory.Faker("sentence", nb_words=3)
    image = factory.LazyAttribute(lambda x: cache_image(300, 300, keyword="clothing"))
    buyer = factory.Faker("company")


class ComplianceSectionFactory(BaseFactory):
    class Meta:
        model = ComplianceSection

    page = factory.SubFactory(CompliancePageFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=10)
    image = factory.LazyAttribute(lambda x: cache_image(600, 400, keyword="factory"))


class ComplianceCertificateFactory(BaseFactory):
    class Meta:
        model = ComplianceCertificate

    page = factory.SubFactory(CompliancePageFactory)
    name = factory.Faker("company")
    image = factory.LazyAttribute(
        lambda x: cache_image(200, 200, keyword="certificate")
    )


class SustainabilitySectionFactory(BaseFactory):
    class Meta:
        model = SustainabilitySection

    page = factory.SubFactory(SustainabilityPageFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=10)
    image = factory.LazyAttribute(
        lambda x: cache_image(600, 400, keyword="sustainable")
    )


class SustainabilityCertificateFactory(BaseFactory):
    class Meta:
        model = SustainabilityCertificate

    page = factory.SubFactory(SustainabilityPageFactory)
    name = factory.Faker("company")
    image = factory.LazyAttribute(
        lambda x: cache_image(200, 200, keyword="certificate")
    )


class GallerySectionFactory(BaseFactory):
    class Meta:
        model = GallerySection

    page = factory.SubFactory(GalleryPageFactory)
    name = factory.Faker(
        "random_element", elements=["Products", "Factory", "Team", "Events"]
    )


class GalleryImageFactory(BaseFactory):
    class Meta:
        model = GalleryImage

    section = factory.SubFactory(GallerySectionFactory)
    caption = factory.Faker("sentence", nb_words=5)
    image = factory.LazyAttribute(lambda x: cache_image(800, 600, keyword="factory"))


class GalleryVideoFactory(BaseFactory):
    class Meta:
        model = GalleryVideo

    section = factory.SubFactory(GallerySectionFactory)
    caption = factory.Faker("sentence", nb_words=5)
    youtube_url = factory.Faker(
        "random_element",
        elements=[
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/8p2e_CIqkJo",
            "https://www.youtube.com/embed/7NOSDKb0HlU",
            "https://www.youtube.com/embed/L_LUpnjgPso",
        ],
    )
