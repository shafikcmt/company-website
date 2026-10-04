# About CMS hardening implementation notes

Current production status: see [PRODUCTION_HARDENING_VALIDATION.md](PRODUCTION_HARDENING_VALIDATION.md). That follow-up supersedes the historical image-cleanup and footer-contact limitations below; the completed About UI/CMS work remains intact.

This pass implements the safe CMS work identified by ABOUT_CONTENT_READINESS_AUDIT.md. That audit remains a historical snapshot; the behavior changes below supersede its ordering, image-limit and social-fallback findings.

## Implemented

- About KPIs explicitly use the four lowest CompanyStats primary keys. The standalone Admin shows IDs and sorts by ID; its inline uses the same ordering. There is no manual KPI order field. The homepage queryset is unchanged.
- About team and FAQ queries use existing order, then primary key as a deterministic tie-breaker. Their standalone/inline editors use the same ordering. Existing list editing, filters and search are preserved; KPI search is added.
- Form-only labels/help text in hapl/admin_content.py explain management versus staff (both public), metric definitions, order, section-selection behavior, unused biography/email fields and public versus legacy site copy. No model labels or data were rewritten. FAQ inline now uses the existing Unfold rich-text widget, as its standalone editor already did.
- About title and meta description reuse SiteSettings.site_name; existing hero, image alt, CTA, navigation and footer branding already use it. A malformed dash in About metadata was corrected while replacing those lines.
- The shared base footer validates optional social URLs through common/templatetags/public_content.py. Only HTTP(S) URLs accepted by Django URLValidator render. Missing, malformed, # and non-web schemes are omitted; valid configured URL strings are retained. This is syntax validation, not ownership or remote availability verification. Other public pages inheriting this shared footer receive this intentional fix. The separate homepage footer already omits blank links and was not edited in this pass.

## Image pipeline findings and targeted change

AboutSection.image was the source of the 800 x 800 limit, not a global setting. It now specifies max_dimensions=(1920, 1440). Team images remain capped at 400 x 400; other image fields and global settings are unchanged.

Upload path: Admin model form -> model save -> OptimizedImageField.pre_save in common/fields.py -> ImageOptimizer.optimize_image in common/services/image.py -> storage. Only uncommitted/new uploads are optimized. PIL thumbnail() fits within the bounding box, preserves aspect ratio and does not upscale. The default output is WebP at quality 75, with existing settings overrides retained. There is one stored processed image, not a responsive variant or thumbnail collection; no srcset generation exists. Large photographic originals are compressed rather than served directly. Transparent RGBA output uses the existing lossless WebP behavior.

The optimizer replaces the uploaded stream with its processed output: a separate original is not retained. AutoCleanupFieldMixin deletes the previous stored file on replacement/clear and deletion. Its existing pre-save cleanup occurs before the replacement save completes, so administrators should retain source files and storage backups. This global cleanup implementation was not changed. On optimizer exceptions the existing utility logs an error and returns the original upload; this pre-existing fallback is not a strict size guarantee.

Existing database image paths and files are untouched; ordinary edits do not reprocess committed images. The current About image remains 800 x 600. The existing same-photo 1440 x 1080 media/home/about-humana.webp can now be uploaded by an administrator without being reduced to 800 px. No automatic replacement was performed.

No migration is needed for this runtime upload configuration. OptimizedImageField currently does not serialize its custom format/quality/max_dimensions arguments through deconstruct(), and Django makemigrations --check --dry-run reports no changes. Historical migration field instances consequently do not retain these custom parameters; do not use them to assume current upload limits in future data migrations. No change to the shared custom-field serialization was introduced in this scoped pass.

## Deferred decisions

- Publication control: recommend a separately reviewed TeamMember.is_active BooleanField with a default preserving existing visibility, corresponding About queryset filtering and Admin list controls. A migration is required. Consider FAQ publication control separately if editorial drafts are needed. No visibility field or deletion-based workaround was added.
- Footer contacts: SiteSettings has no contact fields. ContactData.address, ContactPhone.number/type/is_primary and ContactEmail.email/is_primary could be reused, but current values are generated (1562 Jesse Loaf / New Karenfort, AK 61412; kortiz@example.org and teresa60@example.org). Publishing them in the footer would be unsafe. Existing hardcoded contact text remains unchanged. After company verification, prefer an agreed ContactData record and explicit primary telephone/email selection. If the footer requires separate contacts, proposed SiteSettings fields are footer_address, footer_phone, footer_email; these would require a migration. No choice of legal address or number was made.
- Naming: SiteSettings.site_name currently uses Ltd while footer_description uses Pvt. Ltd. Company approval is required. Page-specific titles/metadata remain hardcoded in products, sustainability, complience, career, career_apply, activities, customers, gallery and contact templates; the base fallback metadata also names Humana Apparels Ltd. Existing fallback brand strings remain. No global replacement or rewriting of stored prose occurred.
- Core values: the six core_values entries are static, defined only in about(). WhyUsFeature is used for a different homepage purpose and is not a clean replacement. Copy and models remain unchanged; company approval is still required.
- Content readiness: replace generated story, KPI data, team roster/photos and FAQs only with approved information. The audit inventory remains applicable. No records were saved by this pass.

## Validation

- Django system check: no issues.
- makemigrations --check --dry-run: no changes detected; no migration created.
- 13 automated tests pass (8 existing plus 5 targeted CMS tests). Coverage includes social URL omission/preservation, dynamic naming, missing content/images, queryset ordering, standalone/inline guidance, large/small/portrait image resizing, WebP conversion and no upscaling.
- Read-only authenticated Admin GET rendering: list and change forms for AboutSection, CompanyStats, TeamMember, TeamSection, FAQ, FAQSection and SiteSettings all return 200, including inlines. Used an existing administrator without login/session/database writes.
- About renders successfully with the current database; missing YouTube is omitted; current About and all team media files verify successfully with Pillow.
- No styling changes, dependency additions, content replacement, commits or pushes. Existing unrelated workspace edits were preserved.

- Browser regression: 360, 390, 768, 1024, 1280, 1440 and 1920 px passed without horizontal overflow; media, FAQ keyboard interaction, CTA destinations, reduced motion and no-JavaScript rendering passed.
