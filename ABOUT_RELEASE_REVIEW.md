# About: final content preparation and release review

Reviewed 2026-10-01 against the current implementation, ABOUT_CONTENT_READINESS_AUDIT.md and ABOUT_CMS_HARDENING.md. The hardening document supersedes historical ordering/image/social findings in the original audit. This review changes documentation only. No records, media, application code, migrations, commits or pushes were changed.

Follow-up status: [PRODUCTION_HARDENING_VALIDATION.md](PRODUCTION_HARDENING_VALIDATION.md) supersedes this historical review's Tailwind CDN, footer-contact and destructive image-cleanup findings. Content approval and staging hosting acceptance remain required.

## Release decision

The About implementation passes local functional, responsive and Admin smoke tests. It is ready for approved content entry and staging acceptance, but NOT cleared for public launch today. Demo content and unverified contacts remain. Content entry alone is not a complete production sign-off: the shared base still loads the Tailwind development CDN, which produces an explicit production warning. Production static/media serving must also be verified in staging. No shared build refactor was performed during this review.

## Final content collection checklist

Every supplied item should have an owner, approval date and authoritative source recorded in the content handoff. These approval details are handoff documentation, not new CMS fields.

| Required item | Supply before launch | Where it goes / constraints |
|---|---|---|
| Company identity | Official legal name; public brand name; approved tagline | SiteSettings.site_name is the public name; site_tagline is the tagline. There are not separate public/legal-name fields in the current public template. Approve the exact legal name used in footer_description and footer_copyright. Legacy company_name is not the public branding source. Resolve Ltd versus Pvt. Ltd. |
| About story | Title; subtitle; intro; 2–3 approved paragraphs | AboutSection #3: title, subtitle, content. There is no separate intro field: use the first paragraph of content, followed by the story paragraphs. Do not duplicate the subtitle. Use simple paragraphs/lists, no pasted font styles or unverified claims. |
| Four KPIs | For each: label, value, unit, time/reference period, approval/source | CompanyStats #9–12: title, value, icon. Unit/reference period must be included clearly in the existing label/value where needed; no dedicated source/date fields exist. Keep evidence in the approved handoff. Do not reinterpret the demo values. |
| Team | Full name; designation; management/staff placement; distinct display order; approved portrait and publishing permission | TeamMember.name, position, is_management, order, image. All entries are public; false means staff, not hidden. Optional verified LinkedIn link for management. All current 15 demo-looking records need review, not just the first five. |
| FAQ | Each question; approved factual answer; distinct order | FAQ.question, answer, order. All five existing generated pairs require replacement with verified material. All entries appear; section association is not a visibility switch. |
| Contact | Verified public phone; email; full address; identify office versus factory | Current About footer contact block is hardcoded in base.html. Entering ContactData/ContactPhone/ContactEmail does NOT update it. After verification, arrange the already-documented scoped wiring/replacement before launch. |
| Social | Official Facebook, LinkedIn, YouTube and Instagram HTTPS URLs, or explicit instruction to omit an unavailable channel | SiteSettings URL fields. About/shared footer omits blank/invalid URLs. Validate ownership and live destinations manually; syntax validation does not verify ownership. Twitter is an Admin field but is not displayed by the current About/home footers. |
| Hero / story / factory imagery | Approved photograph(s), usage permission, source originals and crop approval | AboutSection.image controls BOTH hero and story. Approve one image suitable for both crops; separate hero/story uploads are not currently supported. Current file is only 800×600. |
| Team portraits | Consistent square portraits, official identities, permission | TeamMember.image; avoid demo images or photos reused for different people. |
| Core values | Approval/rejection of all six titles and descriptions | Integrity, Quality, Sustainability, People First, Reliability, Innovation are static in about(). Approval does not require a schema change; requested copy corrections would require a subsequent scoped code edit. |
| Shared footer copy | Approved concise company description and copyright/legal wording | SiteSettings.footer_description and footer_copyright. Confirm ownership, location, product and sustainability claims; maintain the literal copyright year. |
| Brand assets | Approved logo/favicon and permitted use | SiteSettings.site_logo/site_favicon. This is shared branding; not required to replace existing approved assets. |

Current content blockers remain the generated story, four meaningless KPIs, 15 demo-looking team identities with identical dandelion photos, five generated FAQ pairs, placeholder footer phone and unverified address/email, inconsistent legal name, unapproved business/core-value claims, and low-resolution About image.

## Shared-content impact map

**Changing this affects multiple pages.** Apply this warning to every shared row below. Recheck About, Home, and at least one other page inheriting the shared header/footer after population.

| Field(s) | Actual usage / impact |
|---|---|
| SiteSettings.site_name | About title/meta description, hero label, story image alt/caption and CTA; shared navigation logo alt/name and footer; homepage title, hero labels, navigation/footer and captions. Other page-specific titles/metadata can remain hardcoded and will NOT automatically follow the new name. |
| SiteSettings.site_tagline | Shared footer tagline; homepage hero heading fallback only when the configured hero title is absent. |
| SiteSettings.site_logo | Shared navbar and homepage navbar/footer image. Site name controls its dynamic alt text. It does not change the words embedded in the artwork. |
| SiteSettings.site_favicon | Favicon partial used through the shared base, including Home/About. The existing settings/favicon.webp value uses the bundled fallback favicon path. |
| SiteSettings.footer_description | Shared footer, separate homepage footer AND homepage meta description (tags stripped for metadata). Editing it affects search snippets as well as visible prose. |
| SiteSettings.footer_copyright | Shared footer and separate homepage footer; nonempty text is shown literally rather than receiving an automatic year update. |
| SiteSettings.facebook_url/linkedin_url/youtube_url/instagram_url | About and other shared-base footers plus the separate homepage footer. Shared-base footer filters invalid URLs; homepage only checks nonempty values. Keep all configured URLs valid and company-approved. |
| CompanyStats.title/value | About’s first four records; homepage fallback stats when compliance company facts are absent. Current homepage HAS compliance facts and therefore does not visibly show these stats, but changing them still changes its fallback data. |
| CompanyStats.icon | About KPI icon; current homepage fallback displays title/value only. Do not imply changing an icon alters the visible homepage. |
| CompanyStats.section | Existing stats Admin relationship; does not determine About selection or filter Home’s all-record queryset. |
| NavbarSettings.show_* | Shared navigation, including links to About and other routes; not an About content publication switch. |

AboutSection.title/subtitle/content/image are used by the active About route, not the current homepage: Home uses HomeIntroductionSection, a different record and image path. An older partial references an about context but is not included by current routed www templates. Do not confuse the two similar photos.

TeamSection.title/subtitle, TeamMember.name/position/image/order/is_management and management linkedin_url are currently About-only. TeamMember.bio/email and staff LinkedIn are not displayed. FAQSection.title/subtitle and FAQ.question/answer/order are About-only. Core values are About-only. No changes to these create an automatic homepage team/FAQ section.

SiteSettings legacy company_name/logo/favicon/footer_text and twitter_url are not the corresponding rendered About public fields. SiteSettings availability in every template does not mean every field is rendered. Footer phone/address/email and base fallback metadata are hardcoded; do not promise that saving SiteSettings or ContactData updates them.

## Final Admin review and ordering

Read-only list/change rendering passed for AboutSection, CompanyStats, TeamMember, TeamSection, FAQ, FAQSection and SiteSettings, including inlines. Existing labels/help text accurately describe the controls; no further label changes were needed. A non-technical editor with the appropriate model permissions can populate these existing fields, subject to the documented limits. This validates Admin behavior, not a usability study or the permissions of a future editorial account.

- Edit the existing lowest-ID AboutSection/TeamSection/FAQSection records (#3 here). Additional section records do not replace the first section automatically.
- About KPIs are the four lowest CompanyStats IDs, currently 9–12, in ascending ID order. Admin shows IDs. There is no drag/drop or manual KPI order control. Edit those four records; creating a fifth is not a selection mechanism.
- Team members: ascending order, then primary key, within management and staff groups. All current order values are 0; use distinct values such as a spaced sequence chosen by the editor.
- FAQ: ascending order, then primary key. All current order values are 0; use distinct values.
- Team/FAQ changes publish directly. Neither has a draft or visibility toggle. Do not use deletion as an undoable hide action; deletion/file cleanup can be destructive.
- SiteSettings changes are shared immediately. Use Public company name, public footer fields and Social Links, not legacy branding fields.
- Core values and footer contacts are exceptions: they cannot be populated through the current relevant Admin forms alone.

## Future KPI improvement — documentation only

Recommended minimal explicit model extension: CompanyStats.show_on_about (BooleanField) and about_display_order (PositiveIntegerField). The About-specific name avoids implying that homepage order changes. A generic display_order is acceptable only if its About-only scope is clearly documented.

Use a separately approved schema/data migration: default show_on_about=False for future records; backfill True only for the four current lowest-PK records and give them ascending about_display_order values matching the current display. Leave all other records and metric content unchanged. About then selects filter(show_on_about=True).order_by('about_display_order', 'pk')[:4]. Explain the four-item limit and warn editors if more than four are selected; the ordering/tie-breaker makes the result explicit.

Keep the homepage queryset and its compliance-facts/fallback choice unchanged. Do not add global Meta.ordering, do not filter the Home queryset on show_on_about, and do not move or copy metric values. Add Admin list editing/filtering and tests for selection, ties, no selection and unchanged homepage fallback. No migration or implementation was performed now. Current deterministic ID selection is an editorial limitation, not a rendering failure.

## Image readiness and practical handoff guidance

Verified runtime: About cap 1920×1440; team cap 400×400. Current local Django ImageField/Pillow environment accepted JPEG, PNG, WebP and AVIF in in-memory checks. Prefer JPEG/WebP for photographs; decoder availability can differ on production, so verify its installed Pillow/codecs. The optimizer supports WebP/AVIF output; current settings produce WebP at quality 75. Transparent RGBA follows existing lossless WebP handling.

Aspect ratio is preserved using a bounding-box resize. No upscaling. Large landscape and portrait images and small inputs passed the existing tests. One processed file is stored: no responsive srcset variants or retained source original. Existing committed images are not reprocessed during ordinary text edits. Replacements/clears delete the old file through the existing pre-save cleanup; this happens before the replacement save completes and is not rollback-safe. Keep independent originals and database/media backups. On processing failure the utility logs and returns the original upload, so the cap is not an absolute enforcement guarantee.

Recommended preparation targets (guidance, not configured hard upload limits):

- Hero/story: genuine landscape source around 1920×1440, or a larger original pre-sized to that range. Prefer roughly 0.3–2 MB upload; inspect the resulting WebP visually and aim for roughly 150–500 KB where quality permits. Do not upscale the current 800×600 file. An existing 1440×1080 copy of the same image is available at media/home/about-humana.webp, but no media was changed.
- Portraits: consistent 800×800 source files, roughly 100–500 KB each; stored at up to 400×400. Keep eyes/head and shoulders within the central crop-safe region for both square and circular displays. Aim for roughly 20–80 KB stored portraits where quality permits.
- Hero crop: leave quiet space on the left for the heading; retain the main person/action across wide desktop and narrow mobile crops. Do not embed text/logos into the photograph. Review both hero and story because they share one file. Confirm usage rights and subject permission.

## Final smoke results

- Django system checks: no issues.
- Existing and CMS tests: 13 passed.
- makemigrations --check --dry-run: no changes detected; no migration generated.
- Seven relevant Admin model list/change GETs rendered successfully using an existing administrator without saving records.
- About browser checks passed at 360, 390, 640, 768, 820, 1024, 1199, 1200, 1280, 1440 and 1920 px; no horizontal overflow.
- Empty/sparse content and missing image-field variants rendered at 360/768/1440 px; no database edits. An absent image field falls back gracefully; this is not a guarantee for a nonempty field pointing to a deleted/corrupt file.
- FAQ Enter/Space operation, rapid toggling, mobile menu expanded state/Escape focus restoration, no-JavaScript navigation/FAQ, and reduced-motion settings passed.
- Current media loaded successfully; image files verified with Pillow. CTA destinations and every internal footer destination returned HTTP 200.
- Invalid/blank/#/non-web social URLs omitted and valid URL preservation covered by automated tests. External social ownership/availability and tel/mail delivery were not verified; company validation remains required.
- No JavaScript runtime or browser console errors observed. The console DOES warn that cdn.tailwindcss.com should not be used in production. Existing shared runtime Tailwind CDN remains; switching to a verified compiled asset is a separate shared deployment task, not a page redesign.
- Observed initial cumulative layout shift approximately 0.0029 in local Chromium. This is a local smoke measurement, not a field performance guarantee or full cross-browser certification.

## Exact pre-commit / pre-push steps

1. Obtain one signed-off content handoff covering every checklist row, including legal name, sources for KPIs, contact details, social ownership and image permissions. Resolve the demo-content inventory completely.
2. Back up the database and media; retain original uploaded files independently. Use staging for content entry and ensure the editor has only the needed Admin permissions.
3. Update existing records in the documented order, upload approved images, and set distinct team/FAQ order values. Do not add draft records to public lists. Record approval/source details outside the current schema.
4. Obtain a scoped implementation for verified footer contact wiring and any approved core-value copy changes. Do not attempt to solve those by editing unrelated or legacy Admin fields. Confirm legal names in remaining hardcoded page titles before a site-wide launch.
5. Complete a separately scoped production asset/deployment check: compile and serve the shared Tailwind styles rather than the development CDN; verify static collection/media URLs, production settings, installed image codecs and media backups. Do not deploy the development server or assume local DEBUG media serving proves production hosting.
6. Re-run system checks, the full available tests, Admin checks and responsive smoke checks after final content entry. Recheck Home, footer, metadata and other shared consumers. Verify external social/contact destinations with the company.
7. Review git diff and git diff --check. This workspace already contains homepage/base/tests edits from earlier work: inspect and stage only the explicitly approved release files, including required new CSS/JS/template-tag modules. Do not blindly stage all files.
8. Prepare a concrete release diff and content/deployment checklist for approval. Database records/media are not included by a Git commit (media is ignored here); plan their approved transfer separately. Commit/push only after explicit instruction. Neither action was performed in this review.

## Final answer to readiness question

The About UI/CMS is technically stable for approved content entry. It can be production-ready after approved content is populated AND the verified footer-contact/code exceptions and shared production asset/deployment checks above are completed. Approved Admin content alone does not remove those remaining release gates. No new About UI regression was found; the shared Tailwind CDN warning and existing image replacement/failure behaviors remain documented limitations, not silently fixed in this review.
