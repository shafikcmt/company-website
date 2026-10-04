"""Form-only guidance shared by standalone and inline content editors.

Keep labels/help here rather than changing model metadata or database state.
"""
SECTION_HELP = (
    "About uses the section with the lowest record ID. Edit that existing section "
    "rather than creating another. Entries are not publication drafts."
)
ORDER_HELP = "Lower numbers appear first; equal values use record ID. Use distinct values for an intentional sequence."
FIELD_GUIDANCE = {
    "AboutSection": {
        "title": ("Story heading", SECTION_HELP),
        "subtitle": ("Story introduction", "One short, company-approved introduction. Do not include unverified history or leadership claims."),
        "content": ("Company story", "Use approved company copy and simple paragraphs/lists. This rich text is published on About."),
        "image": ("Story image", "Shown beside the company story, and as the page banner when no banner image is set. Upload a crop-safe landscape image, ideally 1920 x 1440. New uploads fit within 1920 x 1440 without upscaling and are compressed to WebP. Keep source originals separately. Previous processed images are retained for rollback safety and cleaned up through a separate maintenance process."),
    },
    "CompanyStats": {
        "number": ("Number", "Animated count-up value, e.g. 2400. Use an approved, verifiable figure."),
        "prefix": ("Prefix", "Optional text before the number, e.g. $."),
        "suffix": ("Suffix", "Optional unit after the number, e.g. +, K or %."),
        "label": ("Label", "Readable description shown under the number, including the unit or period where needed."),
        "title": ("Legacy label", "Kept for backwards compatibility; Label is used when set."),
        "value": ("Legacy display value", "Shown only when Number is empty (e.g. values such as 1.5M). Kept in sync when Number is set."),
        "icon": ("Metric icon", "Optional existing Phosphor class, for example ph-users. Match the verified metric."),
        "order": ("Display order", "Home shows the stats of the first stats section in this order; About shows the first four."),
        "section": ("Stats section", "Home and About use the stats attached to the first (lowest ID) stats section."),
    },
    "TeamMember": {
        "name": ("Full name", "Use the approved public name of a real team member."),
        "position": ("Designation / job title", "Use the company-approved designation."),
        "is_management": ("Display in management group", "Checked: management. Unchecked: staff. Both groups are public; this is NOT a visibility control."),
        "order": ("Display order", ORDER_HELP + " Applied within management/staff groups."),
        "image": ("Portrait", "Use an approved square portrait. Stored uploads fit within 400 x 400; keep originals separately."),
        "section": ("Team section", "All team entries appear on About regardless of section. This association does not hide an entry."),
        "bio": ("Biography", "Not displayed by the current About template."),
        "email": ("Email", "Not displayed by the current About template."),
        "linkedin_url": ("LinkedIn profile", "Optional verified profile; About displays this link for management members only."),
    },
    "FAQ": {
        "question": ("Question", "Use a real buyer question; every FAQ entry is published on About."),
        "answer": ("Approved answer", "Provide a factual company-approved answer using simple paragraphs/lists."),
        "order": ("Display order", ORDER_HELP),
        "section": ("FAQ section", "All FAQ entries appear on About regardless of section; this is not a publication control."),
    },
    "TeamSection": {"title": ("Team heading", SECTION_HELP)},
    "FAQSection": {"title": ("FAQ heading", SECTION_HELP)},
    "SiteSettings": {
        "site_name": ("Public company name", "Used by public branding and the About title/metadata. Confirm the legal/trading name; this does not rewrite prose or other page-specific titles."),
        "footer_description": ("Public footer description", "Use approved company information and a consistent company name. This is the public footer copy, not the legacy Footer text field."),
        "footer_text": ("Footer text (legacy)", "Not used by the public site. Edit Public footer description instead."),
        "footer_copyright": ("Footer copyright", "Use the approved company name. A nonempty value is shown verbatim; when empty the current year is used automatically."),
        "footer_address": ("Footer address", "Published only when filled. Enter a verified public address."),
        "footer_phone": ("Footer phone", "Published only when filled. Enter a verified public number."),
        "footer_email": ("Footer email", "Published only when filled. Enter a verified public address."),
    },
}


class ContentGuidanceMixin:
    """Apply guidance to each generated form field without mutating model fields."""

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        guidance = FIELD_GUIDANCE.get(self.model.__name__, {}).get(db_field.name)
        if guidance:
            kwargs.setdefault("label", guidance[0])
            kwargs.setdefault("help_text", guidance[1])
        return super().formfield_for_dbfield(db_field, request, **kwargs)
