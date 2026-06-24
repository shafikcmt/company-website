from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from common.models import BaseModel
from common.fields import OptimizedImageField


def validate_resume_size(value):
    """Reject resume uploads larger than 5 MB."""
    limit_mb = 5
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(
            f"Resume file too large — maximum size is {limit_mb} MB."
        )


# --- Global Site Settings ---
class SiteSettings(BaseModel):
    """Singleton model holding global site-wide settings."""

    company_name = models.CharField(max_length=200, default="HAPL")
    logo = OptimizedImageField(upload_to="site/", blank=True, null=True)
    favicon = OptimizedImageField(
        upload_to="site/", max_dimensions=(128, 128), blank=True, null=True
    )
    footer_text = models.TextField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    # --- Frontend-facing settings (used by the public site templates) ---
    site_name = models.CharField(max_length=200, default="Humana Apparels Ltd")
    site_tagline = models.CharField(max_length=300, blank=True, null=True)
    site_logo = OptimizedImageField(upload_to="settings/", blank=True, null=True)
    site_favicon = OptimizedImageField(upload_to="settings/", blank=True, null=True)
    footer_description = models.TextField(blank=True, null=True)
    footer_copyright = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name or self.company_name

    def save(self, *args, **kwargs):
        # Enforce singleton: always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class NavbarSettings(BaseModel):
    """Singleton model controlling which navbar links are visible."""

    show_home = models.BooleanField(default=True)
    show_about = models.BooleanField(default=True)
    show_products = models.BooleanField(default=True)
    show_customers = models.BooleanField(default=True)
    show_compliance = models.BooleanField(default=True)
    show_sustainability = models.BooleanField(default=True)
    show_gallery = models.BooleanField(default=True)
    show_activities = models.BooleanField(default=True)
    show_career = models.BooleanField(default=True)
    show_contact = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Navbar Settings"
        verbose_name_plural = "Navbar Settings"

    def __str__(self):
        return "Navbar Settings"

    def save(self, *args, **kwargs):
        # Enforce singleton: always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)


class MailSettings(BaseModel):
    """Singleton model for admin-configurable email settings"""

    career_notification_email = models.EmailField(
        help_text="Where new job application alerts are sent"
    )
    sender_name = models.CharField(
        max_length=100,
        default="Humana Apparels",
        help_text="Display name used as the email sender",
    )
    send_applicant_confirmation = models.BooleanField(
        default=True,
        help_text="Send a confirmation email to applicants on submission",
    )
    send_admin_notification = models.BooleanField(
        default=True,
        help_text="Send a notification email to staff on new applications",
    )

    class Meta:
        verbose_name = "Mail Settings"
        verbose_name_plural = "Mail Settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # prevent deletion of the singleton row

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={"career_notification_email": "careers@humanaapparels.com"},
        )
        return obj

    def __str__(self):
        return "Mail Settings"


class BaseSection(BaseModel):
    """Abstract base model for content sections with title and subtitle"""

    title = models.CharField(max_length=200, null=True, blank=True)
    subtitle = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title or f"{self.__class__.__name__} Section {self.id}"


# --- --- Home Page Models --- ---
class HomeHeroSection(BaseModel):
    """Section model for home page hero/carousel"""

    badge_text = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Small label shown above the title",
    )
    title = models.CharField(max_length=300, blank=True, null=True)
    subtitle = models.CharField(max_length=500, blank=True, null=True)

    cta_primary_text = models.CharField(max_length=100, blank=True, null=True)
    cta_primary_url = models.CharField(max_length=200, blank=True, null=True)
    cta_primary_active = models.BooleanField(default=True)

    cta_secondary_text = models.CharField(max_length=100, blank=True, null=True)
    cta_secondary_url = models.CharField(max_length=200, blank=True, null=True)
    cta_secondary_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Hero Section {self.id}"


class HomeCarouselSlide(BaseModel):
    section = models.ForeignKey(
        HomeHeroSection, related_name="slides", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    image = OptimizedImageField(upload_to="home/carousel/")
    is_active = models.BooleanField(default=True)
    cta_text = models.CharField(max_length=100, blank=True, null=True)
    cta_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title or f"Slide {self.id}"


class HomeIntroductionSection(BaseSection):
    """Section model for home page introduction"""

    content = models.TextField(null=True, blank=True)
    image = OptimizedImageField(upload_to="home/", blank=True, null=True)


class HomeIntroductionFeature(BaseModel):
    introduction = models.ForeignKey(
        HomeIntroductionSection, related_name="features", on_delete=models.CASCADE
    )
    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class HomeServicesSection(BaseSection):
    """Section model for services showcase on home page"""

    pass


class Service(BaseModel):
    section = models.ForeignKey(
        HomeServicesSection,
        related_name="services",
        on_delete=models.CASCADE,
        null=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Phosphor icon class")
    image = OptimizedImageField(
        upload_to="services/", max_dimensions=((800, 800)), blank=True, null=True
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class HomeStatsSection(BaseSection):
    """Section model for company stats on home page"""

    pass


class CompanyStats(BaseModel):
    section = models.ForeignKey(
        HomeStatsSection, related_name="stats", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title


# --- About Page Models ---
class AboutSection(BaseSection):
    """Main about section model"""

    content = models.TextField(null=True, blank=True)
    image = OptimizedImageField(
        upload_to="about/", max_dimensions=(800, 800), blank=True, null=True
    )


class WhyUsSection(BaseSection):
    """Section model for 'Why choose us' features"""

    pass


class WhyUsFeature(BaseModel):
    section = models.ForeignKey(
        WhyUsSection, related_name="features", on_delete=models.CASCADE, null=True
    )
    icon = models.CharField(max_length=50, help_text="Phosphor icon class")
    title = models.CharField(max_length=200)
    description = models.TextField()
    stat_number = models.CharField(max_length=50, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class TeamSection(BaseSection):
    """Section model for team members"""

    pass


class TeamMember(BaseModel):
    section = models.ForeignKey(
        TeamSection, related_name="members", on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = OptimizedImageField(upload_to="team/", max_dimensions=(400, 400))
    is_management = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class FAQSection(BaseSection):
    """Section model for frequently asked questions"""

    pass


class FAQ(BaseModel):
    section = models.ForeignKey(
        FAQSection, related_name="faqs", on_delete=models.CASCADE, null=True
    )
    question = models.CharField(max_length=200)
    answer = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question


# --- Customers Page Models ---
class CustomersSection(BaseSection):
    """Section model for customer showcase"""

    pass


class Customer(BaseModel):
    section = models.ForeignKey(
        CustomersSection, related_name="customers", on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=100)
    logo = OptimizedImageField(upload_to="customers/", max_dimensions=(200, 200))
    url = models.URLField()
    is_featured = models.BooleanField(default=False, help_text="Display on home page")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class TestimonialsSection(BaseSection):
    """Section model for client testimonials"""

    pass


class Testimonial(BaseModel):
    section = models.ForeignKey(
        TestimonialsSection,
        related_name="testimonials",
        on_delete=models.CASCADE,
        null=True,
    )
    content = models.TextField()
    author = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company_logo = OptimizedImageField(
        upload_to="testimonials/", max_dimensions=(100, 100)
    )
    is_featured = models.BooleanField(default=False, help_text="Featured testimonial")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.author


# --- Contact Page Models ---
class ContactSection(BaseSection):
    """Main contact section model"""

    pass


class ContactData(BaseModel):
    section = models.OneToOneField(
        ContactSection, related_name="data", on_delete=models.CASCADE, null=True
    )
    map_title = models.CharField(max_length=200)
    map_subtitle = models.CharField(max_length=500, blank=True, null=True)
    map_image = OptimizedImageField(upload_to="contact/")
    map_url = models.URLField()
    address = models.CharField(max_length=200)
    office_title = models.CharField(max_length=200)
    office_subtitle = models.CharField(max_length=500, blank=True, null=True)
    office_image = OptimizedImageField(upload_to="contact/")
    fax = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.office_title


class ContactMethod(BaseModel):
    """Base model for contact methods (phone, email, etc.)"""

    contact = models.ForeignKey(
        ContactData, related_name="%(class)ss", on_delete=models.CASCADE
    )
    is_primary = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ContactPhone(ContactMethod):
    number = models.CharField(max_length=20)
    type = models.CharField(
        max_length=20,
        choices=(
            ("phone", "Phone"),
            ("whatsapp", "WhatsApp"),
        ),
        default="phone",
    )

    def __str__(self):
        return f"{self.type}: {self.number}"


class ContactEmail(ContactMethod):
    email = models.EmailField()
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.email


class ContactGroup(BaseModel):
    section = models.ForeignKey(
        ContactSection, related_name="groups", on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ContactMember(BaseModel):
    group = models.ForeignKey(
        ContactGroup, related_name="members", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = OptimizedImageField(upload_to="contact/members/", max_dimensions=(400, 400))
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Social(BaseModel):
    section = models.ForeignKey(
        ContactSection, related_name="socials", on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=100)
    url = models.URLField()
    icon = models.CharField(max_length=50, help_text="Phosphor Icon class")

    def __str__(self):
        return self.name


# --- Career Page Models ---
class CareerSection(BaseSection):
    """Section model for career listings"""

    pass


class CareerPosition(BaseModel):
    section = models.ForeignKey(
        CareerSection, related_name="positions", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    posted_at = models.DateField()
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=(("active", "Active"), ("inactive", "Inactive")),
        default="active",
    )
    job_type = models.CharField(
        max_length=20,
        choices=(
            ("full-time", "Full-time"),
            ("part-time", "Part-time"),
            ("contract", "Contract"),
        ),
        default="full-time",
    )
    deadline = models.DateField(blank=True, null=True)
    apply_email = models.EmailField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class JobApplication(BaseModel):
    position = models.ForeignKey(
        CareerPosition, related_name="applications", on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1)
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(
        upload_to="careers/resumes/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"]),
            validate_resume_size,
        ],
        help_text="PDF, DOC or DOCX, up to 5 MB.",
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ("new", "New"),
            ("reviewed", "Reviewed"),
            ("shortlisted", "Shortlisted"),
            ("rejected", "Rejected"),
            ("hired", "Hired"),
        ),
        default="new",
    )

    def __str__(self):
        return f"{self.full_name} - {self.position.title}"


# --- Activities Page Models ---
class ActivitiesSection(BaseSection):
    """Section model for company activities (CSR, events, compliance initiatives)"""

    pass


class Activity(BaseModel):
    section = models.ForeignKey(
        ActivitiesSection, related_name="activities", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=500)
    content = models.TextField(null=True, blank=True)
    image = OptimizedImageField(upload_to="activities/", max_dimensions=(1000, 1000))
    activity_date = models.DateField()
    tag = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Short label shown on the card, e.g. 'CSR', 'Compliance', 'Training'",
    )
    is_featured = models.BooleanField(default=False, help_text="Feature on home page")

    def __str__(self):
        return self.title


# --- Products Page Models ---
class ProductsPage(BaseSection):
    """Main products page model"""

    pass


class ProductCarouselSlide(BaseModel):
    """Carousel slides for products page"""

    page = models.ForeignKey(
        ProductsPage, related_name="carousel_slides", on_delete=models.CASCADE
    )
    image = OptimizedImageField(upload_to="products/carousel/")
    alt = models.CharField(max_length=100)

    def __str__(self):
        return self.alt


class ProductSection(BaseModel):
    """Product sections with text and image"""

    page = models.ForeignKey(
        ProductsPage, related_name="sections", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = OptimizedImageField(upload_to="products/sections/")
    after_products = models.BooleanField(
        default=False, help_text="Display this section after the product portfolio"
    )

    def __str__(self):
        return self.title


class ProductCategory(BaseModel):
    """Product categories (e.g., Jackets, Pants)"""

    page = models.ForeignKey(
        ProductsPage, related_name="categories", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    """Individual product model"""

    category = models.ForeignKey(
        ProductCategory, related_name="products", on_delete=models.CASCADE
    )
    gender = models.CharField(
        max_length=20,
        choices=(("Male", "Male"), ("Female", "Female")),
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200)
    image = OptimizedImageField(upload_to="products/items/")
    buyer = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


# --- Compliance Page Models ---
class CompliancePage(BaseSection):
    """Main compliance page model"""

    pass


class ComplianceSection(BaseModel):
    """Compliance information sections"""

    page = models.ForeignKey(
        CompliancePage, related_name="sections", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = OptimizedImageField(upload_to="compliance/sections/")

    def __str__(self):
        return self.title


class ComplianceCertificate(BaseModel):
    """Certificates for compliance page"""

    page = models.ForeignKey(
        CompliancePage, related_name="certificates", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    image = OptimizedImageField(upload_to="compliance/certificates/")
    website_url = models.URLField(
        blank=True,
        null=True,
        help_text="Optional external link opened when the certification is clicked.",
    )
    is_active = models.BooleanField(
        default=True, help_text="Only active certifications are shown on the site."
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order (ascending)")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class ComplianceCompanyInfo(BaseModel):
    """Editable header (title + description) for the 'Company Information' section."""

    page = models.OneToOneField(
        CompliancePage, related_name="company_info", on_delete=models.CASCADE
    )
    eyebrow = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="At a Glance",
        help_text="Small label shown above the section title.",
    )
    title = models.CharField(max_length=200, default="Company Information")
    description = models.TextField(
        blank=True, null=True, help_text="Optional intro text below the title."
    )

    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.title


class CompanyInfoStat(BaseModel):
    """Individual stat card (e.g. Established, Area, Manpower) for the company info section."""

    page = models.ForeignKey(
        CompliancePage, related_name="company_stats", on_delete=models.CASCADE
    )
    icon = models.CharField(
        max_length=50,
        default="ph-info",
        help_text="Phosphor icon class, e.g. ph-calendar-blank",
    )
    label = models.CharField(max_length=100, help_text="e.g. Established")
    value = models.CharField(max_length=100, help_text="e.g. 1986")
    subtext = models.CharField(
        max_length=100, blank=True, null=True, help_text="Optional smaller line, e.g. 13,577 sq m"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label}: {self.value}"


class CompanyBuyer(BaseModel):
    """Main buyer badge for the company info section."""

    page = models.ForeignKey(
        CompliancePage, related_name="buyers", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    percentage = models.CharField(
        max_length=20, blank=True, null=True, help_text="e.g. 60%"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class ProductionStep(BaseModel):
    """Production process step for the company info section."""

    page = models.ForeignKey(
        CompliancePage, related_name="production_steps", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, help_text="e.g. Cutting")
    note = models.CharField(
        max_length=200, blank=True, null=True, help_text="Optional note, e.g. (Quilting, Downfilling)"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


# --- Sustainability Page Models ---
class SustainabilityPage(BaseSection):
    """Main sustainability page model"""

    pass


class SustainabilitySection(BaseModel):
    """Sustainability information sections"""

    page = models.ForeignKey(
        SustainabilityPage, related_name="sections", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = OptimizedImageField(upload_to="sustainability/sections/")

    def __str__(self):
        return self.title


class SustainabilityCertificate(BaseModel):
    """Certificates for sustainability page"""

    page = models.ForeignKey(
        SustainabilityPage, related_name="certificates", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    image = OptimizedImageField(upload_to="sustainability/certificates/")

    def __str__(self):
        return self.name


# --- Gallery Page Models ---
class GalleryPage(BaseSection):
    """Main gallery page model"""

    pass


class GallerySection(BaseModel):
    """Gallery sections (e.g., Product, Culture, Team, Events)"""

    page = models.ForeignKey(
        GalleryPage, related_name="sections", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GalleryImage(BaseModel):
    """Images for gallery page"""

    section = models.ForeignKey(
        GallerySection, related_name="images", on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=200)
    image = OptimizedImageField(upload_to="gallery/images/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.caption


class GalleryVideo(BaseModel):
    """Videos for gallery page"""

    section = models.ForeignKey(
        GallerySection, related_name="videos", on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=200)
    youtube_url = models.URLField(help_text="YouTube embed URL")

    def __str__(self):
        return self.caption


# --- Compliance Audit Status ---
class AuditStatus(BaseModel):
    """Individual audit/certification record for compliance page"""

    page = models.ForeignKey(
        CompliancePage, related_name="audits", on_delete=models.CASCADE
    )
    sl_no = models.PositiveIntegerField(help_text="Display order number")
    name = models.CharField(max_length=200, help_text="Certificate/Audit name")
    certificate_number = models.CharField(max_length=200, blank=True, null=True)
    audit_date = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="e.g. 31/10/2023 or 18 & 19 Jun 2025",
    )
    expiry_date = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="e.g. 21/10/2027 or Running or Initial",
    )
    status = models.CharField(
        max_length=50,
        choices=(
            ("Done", "Done"),
            ("Running", "Running"),
            ("Applied", "Applied"),
            ("Initial Done", "Initial Done"),
        ),
        default="Done",
    )
    result = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="e.g. Certified, GOLD, Verified, B",
    )

    class Meta:
        ordering = ["sl_no"]

    def __str__(self):
        return f"{self.sl_no}. {self.name}"
