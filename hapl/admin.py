from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget
from django.db import models
from hapl.models import (
    SiteSettings,
    NavbarSettings,
    MailSettings,
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


class BaseModelAdmin(ModelAdmin):
    """Base admin class that hides tracking fields for all models"""

    exclude = ("created_at", "updated_at", "created_by", "updated_by")
    list_per_page = 20


class BaseInline(StackedInline):
    """Base inline class that hides tracking fields"""

    exclude = ("created_at", "updated_at", "created_by", "updated_by")


class BaseSectionAdmin(BaseModelAdmin):
    """Base admin class for section models with title and subtitle"""

    fieldsets = (
        (
            "Section Settings",
            {
                "fields": ("title", "subtitle"),
            },
        ),
    )


# --- Global Site Settings ---


@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseModelAdmin):
    """Singleton admin: only one SiteSettings instance is allowed."""

    fieldsets = (
        (
            "General",
            {
                "classes": ["tab"],
                "fields": ("site_name", "site_tagline", "site_logo", "site_favicon"),
            },
        ),
        (
            "Footer",
            {
                "classes": ["tab"],
                "fields": ("footer_description", "footer_copyright"),
            },
        ),
        (
            "Branding (legacy)",
            {
                "classes": ["tab"],
                "fields": ("company_name", "logo", "favicon", "footer_text"),
            },
        ),
        (
            "Social Links",
            {
                "classes": ["tab"],
                "fields": (
                    "facebook_url",
                    "twitter_url",
                    "linkedin_url",
                    "instagram_url",
                    "youtube_url",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        # Allow adding only if no instance exists yet
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(NavbarSettings)
class NavbarSettingsAdmin(BaseModelAdmin):
    """Singleton admin controlling navbar link visibility."""

    fieldsets = (
        (
            "Navbar Link Visibility",
            {
                "fields": (
                    ("show_home", "show_about", "show_products"),
                    ("show_customers", "show_compliance", "show_sustainability"),
                    ("show_gallery", "show_activities", "show_career"),
                    ("show_contact",),
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return not NavbarSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(MailSettings)
class MailSettingsAdmin(BaseModelAdmin):
    """Singleton admin for email/notification settings. The changelist
    redirects straight to the single row so staff can't create duplicates."""

    fieldsets = (
        (
            "Notifications",
            {
                "fields": (
                    "career_notification_email",
                    "sender_name",
                    "send_applicant_confirmation",
                    "send_admin_notification",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return not MailSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Always edit the single instance directly (create it if missing).
        obj = MailSettings.load()
        url = reverse("admin:hapl_mailsettings_change", args=[obj.pk])
        return redirect(url)


# --- Home Page Sections ---


class HomeCarouselSlideInline(BaseInline):
    model = HomeCarouselSlide
    extra = 0


@admin.register(HomeHeroSection)
class HomeHeroSectionAdmin(BaseModelAdmin):
    inlines = [HomeCarouselSlideInline]

    fieldsets = (
        (
            "Hero Content",
            {
                "fields": ("badge_text", "title", "subtitle"),
            },
        ),
        (
            "Primary CTA Button",
            {
                "fields": (
                    "cta_primary_text",
                    "cta_primary_url",
                    "cta_primary_active",
                ),
            },
        ),
        (
            "Secondary CTA Button",
            {
                "fields": (
                    "cta_secondary_text",
                    "cta_secondary_url",
                    "cta_secondary_active",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(HomeCarouselSlide)
class HomeCarouselSlideAdmin(BaseModelAdmin):
    list_display = ("title", "is_active")
    list_filter = ("is_active",)


class HomeIntroductionFeatureInline(BaseInline):
    model = HomeIntroductionFeature
    extra = 0


@admin.register(HomeIntroductionSection)
class HomeIntroductionSectionAdmin(BaseSectionAdmin):
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}
    inlines = [HomeIntroductionFeatureInline]

    fieldsets = (
        (
            "Section Settings",
            {
                "fields": ("title", "subtitle"),
            },
        ),
        (
            "Content",
            {
                "fields": ("content", "image"),
            },
        ),
    )

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(HomeIntroductionFeature)
class HomeIntroductionFeatureAdmin(BaseModelAdmin):
    list_display = ("title", "icon")


class ServiceInline(BaseInline):
    model = Service
    extra = 0


@admin.register(HomeServicesSection)
class HomeServicesSectionAdmin(BaseSectionAdmin):
    inlines = [ServiceInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(Service)
class ServiceAdmin(BaseModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


class CompanyStatsInline(BaseInline):
    model = CompanyStats
    extra = 0


@admin.register(HomeStatsSection)
class HomeStatsSectionAdmin(BaseSectionAdmin):
    inlines = [CompanyStatsInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(CompanyStats)
class CompanyStatsAdmin(BaseModelAdmin):
    list_display = ("title", "value", "icon")


# --- About Page Sections ---
@admin.register(AboutSection)
class AboutSectionAdmin(BaseSectionAdmin):
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}

    fieldsets = (
        (
            "Section Settings",
            {
                "fields": ("title", "subtitle"),
            },
        ),
        (
            "Content",
            {
                "fields": ("content", "image"),
            },
        ),
    )

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


class WhyUsFeatureInline(BaseInline):
    model = WhyUsFeature
    extra = 0
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


@admin.register(WhyUsSection)
class WhyUsSectionAdmin(BaseSectionAdmin):
    inlines = [WhyUsFeatureInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(WhyUsFeature)
class WhyUsFeatureAdmin(BaseModelAdmin):
    list_display = ("title", "icon", "stat_number", "order")
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


class TeamMemberInline(BaseInline):
    model = TeamMember
    extra = 0


@admin.register(TeamSection)
class TeamSectionAdmin(BaseSectionAdmin):
    inlines = [TeamMemberInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(TeamMember)
class TeamMemberAdmin(BaseModelAdmin):
    list_display = ("name", "position", "is_management", "order")
    list_editable = ("order",)
    list_filter = ("is_management",)
    search_fields = ("name", "position")


class FAQInline(BaseInline):
    model = FAQ
    extra = 0


@admin.register(FAQSection)
class FAQSectionAdmin(BaseSectionAdmin):
    inlines = [FAQInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(FAQ)
class FAQAdmin(BaseModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)
    search_fields = ("question", "answer")
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


# --- Customers Page Sections ---


class CustomerInline(BaseInline):
    model = Customer
    extra = 0
    fields = ("name", "logo", "url", "is_featured", "order")


@admin.register(CustomersSection)
class CustomersSectionAdmin(BaseSectionAdmin):
    inlines = [CustomerInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(Customer)
class CustomerAdmin(BaseModelAdmin):
    list_display = ("logo_preview", "name", "is_featured", "order", "url")
    list_display_links = ("logo_preview", "name")
    list_editable = ("is_featured", "order")
    list_filter = ("is_featured",)
    search_fields = ("name",)
    fieldsets = (
        (
            "Buyer",
            {
                "fields": ("section", "name", "logo", "url"),
            },
        ),
        (
            "Home Page Display",
            {
                "description": (
                    "Enable 'Display on home page' to show this buyer in the "
                    "'Our Valued Buyers' section on the home page."
                ),
                "fields": ("is_featured", "order"),
            },
        ),
    )

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" alt="{}" '
                'style="height:40px;width:auto;object-fit:contain;" />',
                obj.logo.url,
                obj.name,
            )
        return "—"


class TestimonialInline(BaseInline):
    model = Testimonial
    extra = 0


@admin.register(TestimonialsSection)
class TestimonialsSectionAdmin(BaseSectionAdmin):
    inlines = [TestimonialInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(Testimonial)
class TestimonialAdmin(BaseModelAdmin):
    list_display = ("author", "position", "is_featured")
    list_filter = ("is_featured",)
    search_fields = ("author", "position", "content")
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


# --- Contact Page Sections ---
@admin.register(ContactSection)
class ContactSectionAdmin(BaseSectionAdmin):
    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


class ContactPhoneInline(BaseInline):
    model = ContactPhone
    extra = 0


class ContactEmailInline(BaseInline):
    model = ContactEmail
    extra = 0


@admin.register(ContactData)
class ContactDataAdmin(BaseModelAdmin):
    inlines = [ContactPhoneInline, ContactEmailInline]


@admin.register(ContactPhone)
class ContactPhoneAdmin(BaseModelAdmin):
    list_display = ("number", "type", "is_primary")
    list_filter = ("type", "is_primary")


@admin.register(ContactEmail)
class ContactEmailAdmin(BaseModelAdmin):
    list_display = ("email", "department", "is_primary")
    list_filter = ("is_primary",)


class ContactMemberInline(BaseInline):
    model = ContactMember
    extra = 0


@admin.register(ContactGroup)
class ContactGroupAdmin(BaseModelAdmin):
    inlines = [ContactMemberInline]


@admin.register(ContactMember)
class ContactMemberAdmin(BaseModelAdmin):
    list_display = ("name", "position", "group")
    list_filter = ("group",)


@admin.register(Social)
class SocialAdmin(BaseModelAdmin):
    list_display = ("name", "icon")


# --- Career Page Sections ---


class CareerPositionInline(BaseInline):
    model = CareerPosition
    extra = 0


class JobApplicationInline(TabularInline):
    """Read-only list of applications shown under each CareerPosition. Status
    stays editable so an admin can triage without leaving the position page."""

    model = JobApplication
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ("full_name", "email", "phone", "experience_years", "status", "created_at")
    readonly_fields = ("full_name", "email", "phone", "experience_years", "created_at")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(CareerSection)
class CareerSectionAdmin(BaseSectionAdmin):
    inlines = [CareerPositionInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(CareerPosition)
class CareerPositionAdmin(BaseModelAdmin):
    list_display = ("title", "department", "type", "location", "status", "posted_at")
    list_filter = ("location", "department", "status", "job_type")
    search_fields = ("title", "department", "location")
    inlines = [JobApplicationInline]
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


@admin.register(JobApplication)
class JobApplicationAdmin(BaseModelAdmin):
    """Applicant-submitted data is read-only; only `status` can be changed."""

    list_display = (
        "full_name",
        "position",
        "email",
        "phone",
        "experience_years",
        "status",
        "created_at",
    )
    list_filter = ("status", "position")
    search_fields = ("full_name", "email", "phone")
    list_editable = ("status",)
    readonly_fields = (
        "position",
        "full_name",
        "email",
        "phone",
        "experience_years",
        "cover_letter",
        "resume_download",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Application",
            {
                "fields": (
                    "position",
                    "full_name",
                    "email",
                    "phone",
                    "experience_years",
                    "cover_letter",
                    "resume_download",
                )
            },
        ),
        ("Review", {"fields": ("status",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Resume")
    def resume_download(self, obj):
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener" '
                'class="inline-flex items-center gap-1 text-primary-600 font-semibold hover:underline">'
                "⬇ Download résumé</a>",
                obj.resume.url,
            )
        return "—"

    def has_add_permission(self, request):
        # Applications are created from the public site, not the admin.
        return False


# --- Activities Page Sections ---


class ActivityInline(BaseInline):
    model = Activity
    extra = 0


@admin.register(ActivitiesSection)
class ActivitiesSectionAdmin(BaseSectionAdmin):
    inlines = [ActivityInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(Activity)
class ActivityAdmin(BaseModelAdmin):
    list_display = ("title", "tag", "activity_date", "is_featured")
    list_filter = ("tag", "is_featured", "activity_date")
    search_fields = ("title", "excerpt", "tag")
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


class ProductCarouselSlideInline(BaseInline):
    model = ProductCarouselSlide
    extra = 1


class ProductSectionInline(BaseInline):
    model = ProductSection
    extra = 1
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


class ProductCategoryInline(BaseInline):
    model = ProductCategory
    extra = 1


@admin.register(ProductsPage)
class ProductsPageAdmin(BaseSectionAdmin):
    inlines = [ProductCarouselSlideInline, ProductSectionInline, ProductCategoryInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(ProductCarouselSlide)
class ProductCarouselSlideAdmin(BaseModelAdmin):
    list_display = ("alt", "page")
    list_filter = ("page",)


@admin.register(ProductSection)
class ProductSectionAdmin(BaseModelAdmin):
    list_display = ("title", "page", "after_products")
    list_filter = ("page", "after_products")
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


class ProductInline(BaseInline):
    model = Product
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(BaseModelAdmin):
    list_display = ("name", "page")
    list_filter = ("page",)
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    list_display = ("name", "category", "gender", "buyer")
    list_filter = ("category", "gender")
    search_fields = ("name", "buyer")


# --- Compliance Page Sections ---
class ComplianceSectionInline(BaseInline):
    model = ComplianceSection
    extra = 1
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


class ComplianceCertificateInline(BaseInline):
    model = ComplianceCertificate
    extra = 1


@admin.register(CompliancePage)
class CompliancePageAdmin(BaseSectionAdmin):
    inlines = [ComplianceSectionInline, ComplianceCertificateInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(ComplianceSection)
class ComplianceSectionAdmin(BaseModelAdmin):
    list_display = ("title", "page")
    list_filter = ("page",)
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


@admin.register(ComplianceCertificate)
class ComplianceCertificateAdmin(BaseModelAdmin):
    list_display = ("name", "page")
    list_filter = ("page",)


# --- Sustainability Page Sections ---
class SustainabilitySectionInline(BaseInline):
    model = SustainabilitySection
    extra = 1
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


class SustainabilityCertificateInline(BaseInline):
    model = SustainabilityCertificate
    extra = 1


@admin.register(SustainabilityPage)
class SustainabilityPageAdmin(BaseSectionAdmin):
    inlines = [SustainabilitySectionInline, SustainabilityCertificateInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(SustainabilitySection)
class SustainabilitySectionAdmin(BaseModelAdmin):
    list_display = ("title", "page")
    list_filter = ("page",)
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}


@admin.register(SustainabilityCertificate)
class SustainabilityCertificateAdmin(BaseModelAdmin):
    list_display = ("name", "page")
    list_filter = ("page",)


# --- Gallery Page Sections ---
# Django does not support nested inlines, so GallerySection is managed as its
# own admin (with image/video inlines) and linked from GalleryPage via the
# change link on the section inline below.
class GallerySectionInline(TabularInline):
    model = GallerySection
    extra = 1
    fields = ["name"]
    show_change_link = True  # link to edit each section's images/videos separately


@admin.register(GalleryPage)
class GalleryPageAdmin(BaseSectionAdmin):
    inlines = [GallerySectionInline]

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


class GalleryImageInline(StackedInline):
    model = GalleryImage
    extra = 1
    fields = ["caption", "image"]


class GalleryVideoInline(StackedInline):
    model = GalleryVideo
    extra = 1
    fields = ["caption", "youtube_url"]


@admin.register(GallerySection)
class GallerySectionAdmin(BaseModelAdmin):
    list_display = ("name", "page")
    list_filter = ("page",)
    search_fields = ("name",)
    inlines = [GalleryImageInline, GalleryVideoInline]
    fieldsets = (("Section Info", {"fields": ("page", "name")}),)


@admin.register(GalleryImage)
class GalleryImageAdmin(BaseModelAdmin):
    list_display = ("caption", "section")
    list_filter = ("section",)
    search_fields = ("caption",)
    fieldsets = (("Image Info", {"fields": ("section", "caption", "image")}),)


@admin.register(GalleryVideo)
class GalleryVideoAdmin(BaseModelAdmin):
    list_display = ("caption", "section")
    list_filter = ("section",)
    search_fields = ("caption",)
    fieldsets = (("Video Info", {"fields": ("section", "caption", "youtube_url")}),)


def has_add_permission(self, request):
    return False


def has_delete_permission(self, request, obj=None):
    return False
