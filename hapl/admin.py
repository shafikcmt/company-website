"""Admin for the Humana Apparels CMS (django-unfold + django-simple-history).

Conventions
-----------
* Every admin extends `BaseAdmin` (unfold ModelAdmin + SimpleHistoryAdmin) and
  records `created_by` / `updated_by`, including on inline rows.
* Page and section models that exist once per site use `SingletonAdminMixin`:
  the changelist opens the single row, "add" disappears once it exists and
  rows can't be deleted.
* Parent -> child content is edited through inlines; models that have an
  `order` field are drag-sortable (unfold `ordering_field`).
* Fieldsets are grouped as tabs: Content / Call to action / Media / Settings,
  plus Banner + SEO on page models.
"""

from django.contrib import admin
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from hapl.models import (
    SiteSettings,
    NavbarSettings,
    MailSettings,
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
    ContactMember,
    Social,
    CareerSection,
    CareerPosition,
    JobApplication,
    ActivitiesSection,
    Activity,
    ProductsPage,
    ProductCarouselSlide,
    ProductSection,
    ProductCategory,
    Product,
    CompliancePage,
    ComplianceSection,
    ComplianceCertificate,
    ComplianceCompanyInfo,
    CompanyInfoStat,
    CompanyBuyer,
    ProductionStep,
    AuditStatus,
    SustainabilityPage,
    SustainabilitySection,
    SustainabilityCertificate,
    GalleryPage,
    GallerySection,
    GalleryImage,
    GalleryVideo,
)


TRACKING_FIELDS = ("created_at", "updated_at", "created_by", "updated_by")
RICH_TEXT = {models.TextField: {"widget": WysiwygWidget}}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def thumbnail(file, height=56, rounded=True):
    """Small image preview for list/inline readonly columns."""
    if not file:
        return "—"
    try:
        url = file.url
    except ValueError:
        return "—"
    return format_html(
        '<img src="{}" alt="" loading="lazy" style="height:{}px;width:auto;'
        'max-width:160px;object-fit:cover;border-radius:{};'
        'box-shadow:0 0 0 1px rgba(0,0,0,.06)" />',
        url,
        height,
        "8px" if rounded else "0",
    )


class ImagePreviewMixin:
    """Adds an `image_preview` readonly column for `preview_field`."""

    preview_field = "image"
    preview_height = 56

    @admin.display(description="Preview")
    def image_preview(self, obj):
        return thumbnail(getattr(obj, self.preview_field, None), self.preview_height)


class AuditMixin:
    """Stamp created_by / updated_by on the object and on inline rows."""

    def save_model(self, request, obj, form, change):
        if not change and hasattr(obj, "created_by_id"):
            obj.created_by = request.user
        if hasattr(obj, "updated_by_id"):
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.pk and hasattr(obj, "created_by_id"):
                obj.created_by = request.user
            if hasattr(obj, "updated_by_id"):
                obj.updated_by = request.user
            obj.save()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()


class BaseAdmin(AuditMixin, SimpleHistoryAdmin, ModelAdmin):
    exclude = TRACKING_FIELDS
    list_per_page = 25
    warn_unsaved_form = True
    compressed_fields = True


class SingletonAdminMixin:
    """One row per site: the changelist jumps straight to it."""

    def has_add_permission(self, request, obj=None):
        return super().has_add_permission(request) and not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        opts = self.model._meta
        obj = self.model.objects.order_by("pk").first()
        if obj is not None:
            return redirect(
                reverse(f"admin:{opts.app_label}_{opts.model_name}_change", args=[obj.pk])
            )
        return redirect(reverse(f"admin:{opts.app_label}_{opts.model_name}_add"))


class BaseTabularInline(TabularInline):
    exclude = TRACKING_FIELDS
    extra = 0


class BaseStackedInline(StackedInline):
    exclude = TRACKING_FIELDS
    extra = 0


class SortableMixin:
    ordering_field = "order"
    hide_ordering_field = True


# --- Reusable fieldsets -----------------------------------------------------
def section_content(*extra):
    return (
        "Content",
        {"classes": ["tab"], "fields": ("eyebrow", "title", "subtitle", *extra)},
    )


PAGE_BANNER = (
    "Banner",
    {
        "classes": ["tab"],
        "description": "Heading and image at the top of the page. Leave empty to use the section title.",
        "fields": ("banner_title", "banner_subtitle", "banner_image", "banner_preview"),
    },
)
PAGE_CTA = (
    "Call to action",
    {
        "classes": ["tab"],
        "description": "Closing band at the bottom of the page.",
        "fields": ("cta_title", "cta_text", ("cta_button_text", "cta_button_url")),
    },
)
PAGE_SEO = (
    "SEO",
    {
        "classes": ["tab"],
        "description": "Falls back to the defaults in Site Settings.",
        "fields": ("meta_title", "meta_description"),
    },
)


class PageAdmin(SingletonAdminMixin, BaseAdmin):
    """Singleton page model with Banner / CTA / SEO tabs (PageMixin)."""

    readonly_fields = ("banner_preview",)

    @admin.display(description="Banner preview")
    def banner_preview(self, obj):
        return thumbnail(obj.banner_image, 120)


class SectionAdmin(SingletonAdminMixin, BaseAdmin):
    """Singleton section with eyebrow / title / subtitle."""

    fieldsets = (section_content(),)


# ===========================================================================
# Site settings
# ===========================================================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdminMixin, BaseAdmin):
    readonly_fields = ("logo_preview", "logo_light_preview", "favicon_preview", "og_preview")
    fieldsets = (
        (
            "Branding",
            {
                "classes": ["tab"],
                "fields": (
                    "site_name",
                    "site_tagline",
                    ("site_logo", "logo_preview"),
                    ("logo_light", "logo_light_preview"),
                    ("site_favicon", "favicon_preview"),
                ),
            },
        ),
        (
            "Header",
            {
                "classes": ["tab"],
                "description": "Call-to-action button in the top navigation.",
                "fields": ("header_cta_text", "header_cta_url"),
            },
        ),
        (
            "Footer",
            {
                "classes": ["tab"],
                "description": "Social icons come from Contact → Social links.",
                "fields": (
                    "footer_description",
                    "footer_address",
                    ("footer_phone", "footer_email"),
                    ("footer_links_title", "footer_contact_title", "footer_social_title"),
                    "footer_copyright",
                ),
            },
        ),
        (
            "SEO",
            {
                "classes": ["tab"],
                "fields": ("meta_title", "meta_description", ("og_image", "og_preview")),
            },
        ),
        (
            "Legacy",
            {
                "classes": ["tab"],
                "description": (
                    "Older fields kept for backwards compatibility. Their social "
                    "URLs were copied into Contact → Social links."
                ),
                "fields": (
                    "company_name",
                    "logo",
                    "favicon",
                    "footer_text",
                    "facebook_url",
                    "twitter_url",
                    "linkedin_url",
                    "instagram_url",
                    "youtube_url",
                ),
            },
        ),
    )

    @admin.display(description="Preview")
    def logo_preview(self, obj):
        return thumbnail(obj.site_logo, 40, rounded=False)

    @admin.display(description="Preview")
    def logo_light_preview(self, obj):
        if not obj.logo_light:
            return "—"
        return format_html(
            '<span style="display:inline-block;background:#093E61;padding:6px 10px;border-radius:8px">{}</span>',
            thumbnail(obj.logo_light, 32, rounded=False),
        )

    @admin.display(description="Preview")
    def favicon_preview(self, obj):
        return thumbnail(obj.site_favicon, 32)

    @admin.display(description="Preview")
    def og_preview(self, obj):
        return thumbnail(obj.og_image, 80)


@admin.register(NavbarSettings)
class NavbarSettingsAdmin(SingletonAdminMixin, BaseAdmin):
    fieldsets = (
        (
            "Visible menu items",
            {
                "description": "Contact is shown as the header call-to-action button.",
                "fields": (
                    ("show_home", "show_about", "show_products"),
                    ("show_customers", "show_compliance", "show_sustainability"),
                    ("show_gallery", "show_activities", "show_career"),
                    ("show_contact",),
                ),
            },
        ),
    )


@admin.register(MailSettings)
class MailSettingsAdmin(SingletonAdminMixin, BaseAdmin):
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

    def changelist_view(self, request, extra_context=None):
        # Always edit the single instance directly (create it if missing).
        obj = MailSettings.load()
        return redirect(reverse("admin:hapl_mailsettings_change", args=[obj.pk]))


@admin.register(Social)
class SocialAdmin(BaseAdmin):
    list_display = ("name", "url", "icon", "order")
    search_fields = ("name", "url")
    ordering_field = "order"
    hide_ordering_field = True
    fields = ("section", "name", "url", "icon", "order")


# ===========================================================================
# Home
# ===========================================================================
class HomeCarouselSlideInline(SortableMixin, ImagePreviewMixin, BaseTabularInline):
    model = HomeCarouselSlide
    fields = ("image_preview", "image", "alt_text", "caption", "focal_point", "is_active", "order")
    readonly_fields = ("image_preview",)
    tab = True
    verbose_name = "Slide"
    verbose_name_plural = "Slides"


@admin.register(HomeHeroSection)
class HomeHeroSectionAdmin(BaseAdmin):
    inlines = [HomeCarouselSlideInline]
    list_display = ("__str__", "slide_count", "autoplay", "autoplay_interval", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    fieldsets = (
        (
            "Content",
            {
                "classes": ["tab"],
                "fields": ("badge_text", "title", "highlight_word", "subtitle"),
            },
        ),
        (
            "Call to action",
            {
                "classes": ["tab"],
                "fields": (
                    ("cta_primary_text", "cta_primary_url", "cta_primary_active"),
                    ("cta_secondary_text", "cta_secondary_url", "cta_secondary_active"),
                    "bottom_label",
                    ("bottom_link_text", "bottom_link_url"),
                ),
            },
        ),
        (
            "Settings",
            {
                "classes": ["tab"],
                "description": "Only the first active hero is shown on the home page.",
                "fields": ("is_active", "autoplay", "autoplay_interval"),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_slides=models.Count("slides"))

    @admin.display(description="Slides", ordering="_slides")
    def slide_count(self, obj):
        return obj._slides


@admin.register(HomeCarouselSlide)
class HomeCarouselSlideAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "__str__", "section", "focal_point", "is_active", "order")
    list_display_links = ("image_preview", "__str__")
    list_editable = ("is_active",)
    list_filter = ("is_active", "section")
    search_fields = ("title", "alt_text", "caption")
    ordering_field = "order"
    hide_ordering_field = True
    readonly_fields = ("image_preview",)
    list_select_related = ("section",)
    fieldsets = (
        ("Media", {"fields": ("section", "image", "image_preview", "alt_text", "caption", "focal_point")}),
        ("Settings", {"fields": ("is_active", "order")}),
        (
            "Legacy",
            {"classes": ["collapse"], "fields": ("title", "subtitle", "cta_text", "cta_url")},
        ),
    )


class HomeIntroductionFeatureInline(BaseTabularInline):
    model = HomeIntroductionFeature
    fields = ("icon", "title", "description")
    tab = True
    verbose_name_plural = "Features"


@admin.register(HomeIntroductionSection)
class HomeIntroductionSectionAdmin(ImagePreviewMixin, SingletonAdminMixin, BaseAdmin):
    inlines = [HomeIntroductionFeatureInline]
    formfield_overrides = RICH_TEXT
    readonly_fields = ("image_preview",)
    fieldsets = (
        section_content("content"),
        ("Call to action", {"classes": ["tab"], "fields": ("cta_text", "cta_url")}),
        ("Media", {"classes": ["tab"], "fields": ("image", "image_preview")}),
    )


@admin.register(HomeIntroductionFeature)
class HomeIntroductionFeatureAdmin(BaseAdmin):
    list_display = ("title", "icon", "introduction")
    search_fields = ("title", "description")


class ServiceInline(SortableMixin, ImagePreviewMixin, BaseStackedInline):
    model = Service
    fields = (("title", "icon"), "description", ("image", "image_preview"), "order")
    readonly_fields = ("image_preview",)
    formfield_overrides = RICH_TEXT
    tab = True
    verbose_name_plural = "Services"


@admin.register(HomeServicesSection)
class HomeServicesSectionAdmin(SectionAdmin):
    inlines = [ServiceInline]


@admin.register(Service)
class ServiceAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "title", "icon", "section", "order")
    list_display_links = ("image_preview", "title")
    search_fields = ("title", "description")
    ordering_field = "order"
    hide_ordering_field = True
    formfield_overrides = RICH_TEXT
    readonly_fields = ("image_preview",)


class CompanyStatsInline(SortableMixin, BaseTabularInline):
    model = CompanyStats
    fields = ("icon", "prefix", "number", "suffix", "label", "value", "order")
    tab = True
    verbose_name_plural = "Stats"


@admin.register(HomeStatsSection)
class HomeStatsSectionAdmin(SectionAdmin):
    inlines = [CompanyStatsInline]
    fieldsets = (
        (
            "Content",
            {
                "classes": ["tab"],
                "description": (
                    "The title is used as the accessible heading of the stats strip. "
                    "For each stat, set a number (animated count-up) with optional "
                    "prefix/suffix; 'value' is only used when no number is set."
                ),
                "fields": ("eyebrow", "title", "subtitle"),
            },
        ),
    )


@admin.register(CompanyStats)
class CompanyStatsAdmin(BaseAdmin):
    list_display = ("display_label", "display_value", "icon", "section", "order")
    search_fields = ("label", "title", "value")
    ordering_field = "order"
    hide_ordering_field = True
    fieldsets = (
        ("Content", {"fields": ("section", "icon", ("prefix", "number", "suffix"), "label")}),
        ("Legacy", {"classes": ["collapse"], "fields": ("title", "value")}),
        ("Settings", {"fields": ("order",)}),
    )


# ===========================================================================
# About
# ===========================================================================
@admin.register(AboutSection)
class AboutSectionAdmin(ImagePreviewMixin, PageAdmin):
    formfield_overrides = RICH_TEXT
    readonly_fields = ("banner_preview", "image_preview")
    fieldsets = (
        section_content("content"),
        ("Media", {"classes": ["tab"], "fields": ("image", "image_preview")}),
        PAGE_BANNER,
        PAGE_CTA,
        PAGE_SEO,
    )


class WhyUsFeatureInline(SortableMixin, BaseStackedInline):
    model = WhyUsFeature
    fields = (("icon", "title", "stat_number"), "description", "order")
    formfield_overrides = RICH_TEXT
    tab = True
    verbose_name = "Core value"
    verbose_name_plural = "Core values"


@admin.register(WhyUsSection)
class WhyUsSectionAdmin(SectionAdmin):
    inlines = [WhyUsFeatureInline]


@admin.register(WhyUsFeature)
class WhyUsFeatureAdmin(BaseAdmin):
    list_display = ("title", "icon", "stat_number", "order")
    ordering_field = "order"
    hide_ordering_field = True
    formfield_overrides = RICH_TEXT


class TeamMemberInline(SortableMixin, ImagePreviewMixin, BaseTabularInline):
    model = TeamMember
    fields = ("image_preview", "image", "name", "position", "is_management", "linkedin_url", "order")
    readonly_fields = ("image_preview",)
    tab = True
    show_change_link = True
    verbose_name_plural = "Team members"


@admin.register(TeamSection)
class TeamSectionAdmin(SectionAdmin):
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "name", "position", "is_management", "order")
    list_display_links = ("image_preview", "name")
    list_editable = ("is_management",)
    list_filter = ("is_management",)
    search_fields = ("name", "position")
    ordering_field = "order"
    hide_ordering_field = True
    readonly_fields = ("image_preview",)


class FAQInline(SortableMixin, BaseStackedInline):
    model = FAQ
    fields = ("question", "answer", "order")
    formfield_overrides = RICH_TEXT
    tab = True
    verbose_name_plural = "Questions"


@admin.register(FAQSection)
class FAQSectionAdmin(SectionAdmin):
    inlines = [FAQInline]


@admin.register(FAQ)
class FAQAdmin(BaseAdmin):
    list_display = ("question", "order")
    search_fields = ("question", "answer")
    ordering_field = "order"
    hide_ordering_field = True
    formfield_overrides = RICH_TEXT


# ===========================================================================
# Customers
# ===========================================================================
class CustomerInline(SortableMixin, ImagePreviewMixin, BaseTabularInline):
    model = Customer
    preview_field = "logo"
    fields = ("image_preview", "logo", "name", "url", "is_featured", "order")
    readonly_fields = ("image_preview",)
    tab = True
    verbose_name_plural = "Customers"


@admin.register(CustomersSection)
class CustomersSectionAdmin(PageAdmin):
    inlines = [CustomerInline]
    fieldsets = (section_content(), PAGE_BANNER, PAGE_CTA, PAGE_SEO)


@admin.register(Customer)
class CustomerAdmin(ImagePreviewMixin, BaseAdmin):
    preview_field = "logo"
    preview_height = 40
    list_display = ("image_preview", "name", "is_featured", "url", "order")
    list_display_links = ("image_preview", "name")
    list_editable = ("is_featured",)
    list_filter = ("is_featured",)
    search_fields = ("name",)
    ordering_field = "order"
    hide_ordering_field = True
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Content", {"fields": ("section", "name", "url")}),
        ("Media", {"fields": ("logo", "image_preview")}),
        (
            "Settings",
            {
                "description": "Featured customers appear in the home page logo marquee.",
                "fields": ("is_featured", "order"),
            },
        ),
    )


class TestimonialInline(SortableMixin, ImagePreviewMixin, BaseStackedInline):
    model = Testimonial
    preview_field = "company_logo"
    fields = ("content", ("author", "position"), ("company_logo", "image_preview"), "is_featured", "order")
    readonly_fields = ("image_preview",)
    tab = True
    verbose_name_plural = "Testimonials"


@admin.register(TestimonialsSection)
class TestimonialsSectionAdmin(SectionAdmin):
    inlines = [TestimonialInline]


@admin.register(Testimonial)
class TestimonialAdmin(ImagePreviewMixin, BaseAdmin):
    preview_field = "company_logo"
    list_display = ("image_preview", "author", "position", "is_featured", "order")
    list_display_links = ("image_preview", "author")
    list_editable = ("is_featured",)
    list_filter = ("is_featured",)
    search_fields = ("author", "position", "content")
    ordering_field = "order"
    hide_ordering_field = True
    readonly_fields = ("image_preview",)


# ===========================================================================
# Contact
# ===========================================================================
class ContactDataInline(BaseStackedInline):
    model = ContactData
    max_num = 1
    can_delete = False
    show_change_link = True
    tab = True
    verbose_name = "Office & map"
    verbose_name_plural = "Office & map"
    fields = (
        ("office_title", "office_subtitle"),
        "office_image",
        "address",
        "fax",
        ("map_title", "map_subtitle"),
        "map_url",
        "map_image",
    )


class ContactGroupInline(BaseTabularInline):
    model = ContactGroup
    fields = ("name",)
    show_change_link = True
    tab = True
    verbose_name_plural = "Contact groups"


class SocialInline(SortableMixin, BaseTabularInline):
    model = Social
    fields = ("name", "url", "icon", "order")
    tab = True
    verbose_name_plural = "Social links"


@admin.register(ContactSection)
class ContactSectionAdmin(PageAdmin):
    inlines = [ContactDataInline, ContactGroupInline, SocialInline]
    fieldsets = (
        section_content("groups_title", "groups_empty_text", "socials_title"),
        PAGE_BANNER,
        PAGE_CTA,
        PAGE_SEO,
    )


class ContactPhoneInline(BaseTabularInline):
    model = ContactPhone
    fields = ("number", "type", "is_primary")
    tab = True
    verbose_name_plural = "Phone numbers"


class ContactEmailInline(BaseTabularInline):
    model = ContactEmail
    fields = ("email", "department", "is_primary")
    tab = True
    verbose_name_plural = "Email addresses"


@admin.register(ContactData)
class ContactDataAdmin(BaseAdmin):
    inlines = [ContactPhoneInline, ContactEmailInline]
    list_display = ("office_title", "address", "section")
    readonly_fields = ("office_preview", "map_preview")
    fieldsets = (
        (
            "Office",
            {
                "classes": ["tab"],
                "fields": ("section", "office_title", "office_subtitle", "address", "fax", ("office_image", "office_preview")),
            },
        ),
        (
            "Map",
            {"classes": ["tab"], "fields": ("map_title", "map_subtitle", "map_url", ("map_image", "map_preview"))},
        ),
    )

    @admin.display(description="Preview")
    def office_preview(self, obj):
        return thumbnail(obj.office_image, 80)

    @admin.display(description="Preview")
    def map_preview(self, obj):
        return thumbnail(obj.map_image, 80)


@admin.register(ContactPhone)
class ContactPhoneAdmin(BaseAdmin):
    list_display = ("number", "type", "is_primary", "contact")
    list_filter = ("type", "is_primary")
    list_editable = ("is_primary",)


@admin.register(ContactEmail)
class ContactEmailAdmin(BaseAdmin):
    list_display = ("email", "department", "is_primary", "contact")
    list_filter = ("is_primary",)
    list_editable = ("is_primary",)
    search_fields = ("email", "department")


class ContactMemberInline(ImagePreviewMixin, BaseTabularInline):
    model = ContactMember
    fields = ("image_preview", "image", "name", "position", "email", "phone")
    readonly_fields = ("image_preview",)
    tab = True
    verbose_name_plural = "Members"


@admin.register(ContactGroup)
class ContactGroupAdmin(BaseAdmin):
    inlines = [ContactMemberInline]
    list_display = ("name", "section", "member_count")
    search_fields = ("name",)
    fieldsets = (("Content", {"classes": ["tab"], "fields": ("section", "name")}),)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_members=models.Count("members"))

    @admin.display(description="Members", ordering="_members")
    def member_count(self, obj):
        return obj._members


@admin.register(ContactMember)
class ContactMemberAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "name", "position", "group", "email")
    list_display_links = ("image_preview", "name")
    list_filter = ("group",)
    search_fields = ("name", "position", "email")
    list_select_related = ("group",)
    readonly_fields = ("image_preview",)


# ===========================================================================
# Career
# ===========================================================================
class CareerPositionInline(SortableMixin, BaseStackedInline):
    model = CareerPosition
    fields = (
        ("title", "status"),
        ("department", "location"),
        ("type", "job_type"),
        ("posted_at", "deadline"),
        "description",
        "apply_email",
        "order",
    )
    formfield_overrides = RICH_TEXT
    show_change_link = True
    tab = True
    verbose_name_plural = "Positions"


@admin.register(CareerSection)
class CareerSectionAdmin(PageAdmin):
    inlines = [CareerPositionInline]
    fieldsets = (
        section_content("positions_title", "positions_empty_text"),
        PAGE_BANNER,
        PAGE_CTA,
        PAGE_SEO,
    )


class JobApplicationInline(TabularInline):
    """Read-only list of applications shown under each CareerPosition. Status
    stays editable so an admin can triage without leaving the position page."""

    model = JobApplication
    extra = 0
    can_delete = False
    show_change_link = True
    tab = True
    fields = ("full_name", "email", "phone", "experience_years", "status", "created_at")
    readonly_fields = ("full_name", "email", "phone", "experience_years", "created_at")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(CareerPosition)
class CareerPositionAdmin(BaseAdmin):
    list_display = ("title", "department", "job_type", "location", "status", "posted_at", "deadline")
    list_filter = ("status", "job_type", "department", "location")
    list_editable = ("status",)
    search_fields = ("title", "department", "location")
    date_hierarchy = "posted_at"
    inlines = [JobApplicationInline]
    formfield_overrides = RICH_TEXT
    fieldsets = (
        (
            "Content",
            {
                "classes": ["tab"],
                "fields": ("section", "title", ("department", "location"), ("type", "job_type"), "description"),
            },
        ),
        (
            "Settings",
            {"classes": ["tab"], "fields": ("status", ("posted_at", "deadline"), "apply_email", "order")},
        ),
    )


@admin.register(JobApplication)
class JobApplicationAdmin(BaseAdmin):
    """Applicant-submitted data is read-only; only `status` can be changed."""

    list_display = ("full_name", "position", "email", "phone", "experience_years", "status", "created_at")
    list_filter = ("status", "position")
    search_fields = ("full_name", "email", "phone")
    list_editable = ("status",)
    list_select_related = ("position",)
    date_hierarchy = "created_at"
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


# ===========================================================================
# Activities (news)
# ===========================================================================
class ActivityInline(ImagePreviewMixin, BaseStackedInline):
    model = Activity
    fields = (
        ("title", "tag"),
        "excerpt",
        "content",
        ("image", "image_preview"),
        ("activity_date", "is_featured"),
    )
    readonly_fields = ("image_preview",)
    formfield_overrides = RICH_TEXT
    show_change_link = True
    tab = True
    verbose_name_plural = "Activities"


@admin.register(ActivitiesSection)
class ActivitiesSectionAdmin(PageAdmin):
    inlines = [ActivityInline]
    fieldsets = (section_content(), PAGE_BANNER, PAGE_CTA, PAGE_SEO)


@admin.register(Activity)
class ActivityAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "title", "tag", "activity_date", "is_featured")
    list_display_links = ("image_preview", "title")
    list_editable = ("is_featured",)
    list_filter = ("is_featured", "tag")
    search_fields = ("title", "excerpt", "tag")
    date_hierarchy = "activity_date"
    formfield_overrides = RICH_TEXT
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Content", {"classes": ["tab"], "fields": ("section", "title", "tag", "excerpt", "content")}),
        ("Media", {"classes": ["tab"], "fields": ("image", "image_preview")}),
        (
            "Settings",
            {
                "classes": ["tab"],
                "description": "Featured activities appear on the home page; the first one leads the Activities page.",
                "fields": ("activity_date", "is_featured"),
            },
        ),
    )


# ===========================================================================
# Products
# ===========================================================================
class ProductCarouselSlideInline(SortableMixin, ImagePreviewMixin, BaseTabularInline):
    model = ProductCarouselSlide
    fields = ("image_preview", "image", "alt", "order")
    readonly_fields = ("image_preview",)
    tab = True
    verbose_name_plural = "Banner carousel"


class ProductSectionInline(SortableMixin, ImagePreviewMixin, BaseStackedInline):
    model = ProductSection
    fields = (("eyebrow", "title"), "description", ("image", "image_preview"), "after_products", "order")
    readonly_fields = ("image_preview",)
    formfield_overrides = RICH_TEXT
    tab = True
    verbose_name_plural = "Content sections"


class ProductCategoryInline(SortableMixin, BaseTabularInline):
    model = ProductCategory
    fields = ("name", "product_count", "order")
    readonly_fields = ("product_count",)
    show_change_link = True
    tab = True
    verbose_name_plural = "Categories"

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count() if obj.pk else 0


@admin.register(ProductsPage)
class ProductsPageAdmin(PageAdmin):
    inlines = [ProductCarouselSlideInline, ProductSectionInline, ProductCategoryInline]
    fieldsets = (
        section_content(),
        (
            "Portfolio",
            {"classes": ["tab"], "fields": ("portfolio_eyebrow", "portfolio_title", "portfolio_subtitle")},
        ),
        PAGE_BANNER,
        PAGE_CTA,
        PAGE_SEO,
    )


@admin.register(ProductCarouselSlide)
class ProductCarouselSlideAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "alt", "page", "order")
    list_display_links = ("image_preview", "alt")
    ordering_field = "order"
    hide_ordering_field = True
    readonly_fields = ("image_preview",)


@admin.register(ProductSection)
class ProductSectionAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "title", "after_products", "order")
    list_display_links = ("image_preview", "title")
    list_editable = ("after_products",)
    list_filter = ("after_products",)
    ordering_field = "order"
    hide_ordering_field = True
    formfield_overrides = RICH_TEXT
    readonly_fields = ("image_preview",)


class ProductInline(SortableMixin, ImagePreviewMixin, BaseTabularInline):
    model = Product
    fields = ("image_preview", "image", "name", "gender", "buyer", "order")
    readonly_fields = ("image_preview",)
    tab = True
    verbose_name_plural = "Products"


@admin.register(ProductCategory)
class ProductCategoryAdmin(BaseAdmin):
    list_display = ("name", "page", "product_count", "order")
    search_fields = ("name",)
    ordering_field = "order"
    hide_ordering_field = True
    inlines = [ProductInline]
    fieldsets = (("Content", {"classes": ["tab"], "fields": ("page", "name", "order")}),)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_products=models.Count("products"))

    @admin.display(description="Products", ordering="_products")
    def product_count(self, obj):
        return obj._products


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "name", "category", "gender", "buyer", "order")
    list_display_links = ("image_preview", "name")
    list_filter = ("category", "gender")
    search_fields = ("name", "buyer")
    list_select_related = ("category",)
    readonly_fields = ("image_preview",)


# ===========================================================================
# Compliance
# ===========================================================================
class ComplianceCompanyInfoInline(BaseStackedInline):
    model = ComplianceCompanyInfo
    max_num = 1
    can_delete = False
    fields = ("eyebrow", "title", "description")
    formfield_overrides = RICH_TEXT
    tab = True
    verbose_name_plural = "Company information"


class CompanyInfoStatInline(SortableMixin, BaseTabularInline):
    model = CompanyInfoStat
    fields = ("icon", "label", "value", "subtext", "order")
    tab = True
    verbose_name_plural = "Company stats"


class CompanyBuyerInline(SortableMixin, BaseTabularInline):
    model = CompanyBuyer
    # Percentage is intentionally omitted: it is no longer entered or shown.
    fields = ("name", "order")
    tab = True
    verbose_name_plural = "Main buyers"


class ProductionStepInline(SortableMixin, BaseTabularInline):
    model = ProductionStep
    fields = ("name", "note", "order")
    tab = True
    verbose_name_plural = "Production steps"


class AuditStatusInline(BaseTabularInline):
    model = AuditStatus
    fields = ("sl_no", "name", "certificate_number", "audit_date", "expiry_date", "status", "result")
    ordering = ("sl_no",)
    tab = True
    verbose_name_plural = "Audit status"


class ComplianceSectionInline(SortableMixin, ImagePreviewMixin, BaseStackedInline):
    model = ComplianceSection
    fields = (("eyebrow", "title"), "description", ("image", "image_preview"), "order")
    readonly_fields = ("image_preview",)
    formfield_overrides = RICH_TEXT
    tab = True
    verbose_name_plural = "Standards"


class ComplianceCertificateInline(SortableMixin, ImagePreviewMixin, BaseTabularInline):
    model = ComplianceCertificate
    fields = ("image_preview", "image", "name", "website_url", "is_active", "order")
    readonly_fields = ("image_preview",)
    tab = True
    verbose_name_plural = "Certificates"


@admin.register(CompliancePage)
class CompliancePageAdmin(PageAdmin):
    inlines = [
        ComplianceCompanyInfoInline,
        CompanyInfoStatInline,
        CompanyBuyerInline,
        ProductionStepInline,
        AuditStatusInline,
        ComplianceSectionInline,
        ComplianceCertificateInline,
    ]
    fieldsets = (
        section_content(),
        (
            "Section headings",
            {
                "classes": ["tab"],
                "fields": (
                    ("audit_eyebrow", "audit_title"),
                    "audit_description",
                    "standards_title",
                    "standards_description",
                    ("certificates_eyebrow", "certificates_title"),
                ),
            },
        ),
        PAGE_BANNER,
        PAGE_CTA,
        PAGE_SEO,
    )


@admin.register(ComplianceSection)
class ComplianceSectionAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "title", "page", "order")
    list_display_links = ("image_preview", "title")
    ordering_field = "order"
    hide_ordering_field = True
    formfield_overrides = RICH_TEXT
    readonly_fields = ("image_preview",)


@admin.register(ComplianceCertificate)
class ComplianceCertificateAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "name", "is_active", "website_url", "order")
    list_display_links = ("image_preview", "name")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("name",)
    ordering_field = "order"
    hide_ordering_field = True
    readonly_fields = ("image_preview",)


@admin.register(AuditStatus)
class AuditStatusAdmin(BaseAdmin):
    list_display = ("sl_no", "name", "certificate_number", "audit_date", "expiry_date", "status", "result")
    list_filter = ("status", "result")
    list_editable = ("status",)
    search_fields = ("name", "certificate_number", "result")
    ordering = ("sl_no",)


# ===========================================================================
# Sustainability
# ===========================================================================
class SustainabilitySectionInline(SortableMixin, ImagePreviewMixin, BaseStackedInline):
    model = SustainabilitySection
    fields = (("eyebrow", "title"), "description", ("image", "image_preview"), "order")
    readonly_fields = ("image_preview",)
    formfield_overrides = RICH_TEXT
    tab = True
    verbose_name_plural = "Chapters"


class SustainabilityCertificateInline(SortableMixin, ImagePreviewMixin, BaseTabularInline):
    model = SustainabilityCertificate
    fields = ("image_preview", "image", "name", "order")
    readonly_fields = ("image_preview",)
    tab = True
    verbose_name_plural = "Certificates"


@admin.register(SustainabilityPage)
class SustainabilityPageAdmin(PageAdmin):
    inlines = [SustainabilitySectionInline, SustainabilityCertificateInline]
    fieldsets = (section_content("certificates_title"), PAGE_BANNER, PAGE_CTA, PAGE_SEO)


@admin.register(SustainabilitySection)
class SustainabilitySectionAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "title", "page", "order")
    list_display_links = ("image_preview", "title")
    ordering_field = "order"
    hide_ordering_field = True
    formfield_overrides = RICH_TEXT
    readonly_fields = ("image_preview",)


@admin.register(SustainabilityCertificate)
class SustainabilityCertificateAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "name", "page", "order")
    list_display_links = ("image_preview", "name")
    ordering_field = "order"
    hide_ordering_field = True
    readonly_fields = ("image_preview",)


# ===========================================================================
# Gallery
# ===========================================================================
# Django has no nested inlines: GalleryPage lists its sections, and each
# section's change page manages its images and videos.
class GallerySectionInline(SortableMixin, BaseTabularInline):
    model = GallerySection
    fields = ("name", "image_count", "order")
    readonly_fields = ("image_count",)
    show_change_link = True
    tab = True
    verbose_name_plural = "Sections (filter tabs)"

    @admin.display(description="Images")
    def image_count(self, obj):
        return obj.images.count() if obj.pk else 0


@admin.register(GalleryPage)
class GalleryPageAdmin(PageAdmin):
    inlines = [GallerySectionInline]
    fieldsets = (section_content("all_tab_label", "videos_title"), PAGE_BANNER, PAGE_CTA, PAGE_SEO)


class GalleryImageInline(SortableMixin, ImagePreviewMixin, BaseTabularInline):
    model = GalleryImage
    fields = ("image_preview", "image", "caption", "order")
    readonly_fields = ("image_preview",)
    tab = True
    verbose_name_plural = "Images"


class GalleryVideoInline(SortableMixin, BaseTabularInline):
    model = GalleryVideo
    fields = ("caption", "youtube_url", "order")
    tab = True
    verbose_name_plural = "Videos"


@admin.register(GallerySection)
class GallerySectionAdmin(BaseAdmin):
    list_display = ("name", "page", "image_count", "order")
    search_fields = ("name",)
    ordering_field = "order"
    hide_ordering_field = True
    inlines = [GalleryImageInline, GalleryVideoInline]
    fieldsets = (("Content", {"classes": ["tab"], "fields": ("page", "name", "order")}),)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_images=models.Count("images"))

    @admin.display(description="Images", ordering="_images")
    def image_count(self, obj):
        return obj._images


@admin.register(GalleryImage)
class GalleryImageAdmin(ImagePreviewMixin, BaseAdmin):
    list_display = ("image_preview", "caption", "section", "order")
    list_display_links = ("image_preview", "caption")
    list_filter = ("section",)
    search_fields = ("caption",)
    list_select_related = ("section",)
    readonly_fields = ("image_preview",)
    fieldsets = (("Content", {"fields": ("section", "caption", "image", "image_preview", "order")}),)


@admin.register(GalleryVideo)
class GalleryVideoAdmin(BaseAdmin):
    list_display = ("caption", "section", "youtube_url", "order")
    list_filter = ("section",)
    search_fields = ("caption",)
    list_select_related = ("section",)
    fieldsets = (("Content", {"fields": ("section", "caption", "youtube_url", "order")}),)
