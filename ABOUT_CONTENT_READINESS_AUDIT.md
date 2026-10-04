# About page content readiness audit

Audit date: 2026-10-01. Read-only inspection of current database records, admin registration, view queries, templates, image dimensions and image hashes. No company claims were independently verified. No database, application code, template, image or migration changes were made.

**Readiness: not ready for publication with current content.** The frontend can remain as designed; company-approved content is required.

| Item | Current value / problem | Source and Admin fields | Company input | Recommended format |
|---|---|---|---|---|
| Company story | AboutSection #3 contains generated nonsense. “Our Story” is usable; subtitle “From humble beginnings to a global apparel manufacturing leader.” makes an unverified leadership/history claim. | AboutSection.title, subtitle, content; Admin /admin/hapl/aboutsection/3/change/ | Yes: approved story and substantiation of claims | One short introduction plus 2–3 concise paragraphs; simple rich text, verified dates/capabilities only. |
| KPIs | All four current labels and values are unusable as business facts; globe/calendar icons do not communicate verified metric meanings. | CompanyStats.title, value, icon, section; standalone Admin Company stats or Home stats section inline | Yes: metric definition, approved value, unit/time period and reporting date | Suggested label types only: Years of Experience, Global Customers, Employees, Production Capacity, Export Markets. Do not reuse current numbers for these labels. |
| Leadership and staff | 15 demo-looking identities/roles; all 15 image files have identical SHA-256 hashes. All order values are 0; bio/email/LinkedIn are blank. | TeamMember.name, position, image, order, is_management, linkedin_url, bio, email; standalone Team members or Team section inline | Yes: approved roster, real designations, portraits, publishing consent and order | Consistent square portraits, ideally 800×800 originals; stored upload capped at 400×400. Short official titles. Verified LinkedIn URLs are optional. |
| Section introductions | TeamSection #3: Our Team / Meet the experts behind our success. FAQSection #3: Frequently Asked Questions / Get answers to common questions about our services. Generic but coherent, not nonsense. | TeamSection.title/subtitle and FAQSection.title/subtitle | Approval recommended | Short heading and one supporting sentence; no invented credentials. |
| FAQ | All five question/answer pairs are generated nonsense; all order values are 0. | FAQ.question, answer, order, section; standalone FAQs or FAQ section inline | Yes: company-approved answers | Direct question plus a short factual answer; simple paragraphs/lists. Set distinct order values. |
| Hero and story photograph | Both use AboutSection #3 image=about/about-humana.webp; /media/about/about-humana.webp; 800×600 WebP, 64,342 bytes. Same photograph is available at media/home/about-humana.webp, 1440×1080, 119,914 bytes, visually inspected. | AboutSection.image; templates/www/about.html renders this field twice | Confirm image ownership/consent and approved subject; no new facts needed to reuse the existing photo | Prefer a 1920×1440 landscape original for the dual-use hero/story crop, or larger original; WebP, no baked-in text, subject within crop-safe area. Current field caps uploads to 800×800; increasing retention needs a separately reviewed field configuration change. No replacement made. |
| Footer phone | Visible +880 0000 000000; link tel:+880000000000 is placeholder content. | templates/www/base.html:189; hardcoded, no Admin field controlling this footer phone | Yes: verified public phone number | International display format and corresponding tel: link. ContactPhone edits do not update this template. |
| Footer address/email | Dhaka, Bangladesh and info@humanaapparels.com are hardcoded and unverified. Footer database description instead locates the business in Gorai, Mirzapur, Tangail; clarify office versus factory. | templates/www/base.html contact block; no controlling Admin fields for these displayed values | Yes: approved office/factory address and public email | Use a clearly identified office/factory location and verified mailbox; do not infer from domain. |
| Shared company copy | SiteSettings #1 tagline Premier Garment Manufacturer; description claims joint venture, ownership, location, premium outerwear/technical garments, global brands and ethical/sustainable production. Not nonsense, but factual approval is needed. site_name says Ltd; description says Pvt. Ltd. | SiteSettings.site_name, site_tagline, footer_description | Yes: legal entity name and approval/evidence for business claims | One consistent approved legal/trading name and a concise factual company summary. |
| Footer copyright | Stored value is valid Unicode: © 2026 Humana Apparels Ltd. All rights reserved. Year is fixed at 2026; an initial console display artifact was checked and is not a database encoding defect. | SiteSettings.footer_copyright (not legacy footer_text) | Confirm legal name; no encoding correction required | Retain valid UTF-8, use the approved entity name, and maintain the year. Existing nonempty value bypasses automatic year fallback. |
| Social links | YouTube is blank, but template renders a YouTube anchor with href=#. Facebook, LinkedIn and Instagram URLs are populated; ownership/destinations were not externally verified. | SiteSettings.facebook_url, linkedin_url, instagram_url, youtube_url; base.html renders # for missing values | Yes: approved official profiles or decision to omit unavailable channels | Full official HTTPS profile URLs. Do not invent a YouTube URL. |
| Core values | Integrity, Quality, Sustainability, People First, Reliability, Innovation and descriptions are literal data in views.about(), not database records. | hapl/views.py about() core_values; no Admin field | Yes: approve every statement, especially safe/fair workplace, environmental responsibility and on-time delivery claims | Short approved principle plus one factual commitment. Existing copy may remain only after company approval. |

## Exact replacement inventory

### AboutSection #3 content

```html
<div>Hit put above safe. Once sign many pass. Thought hot relationship couple. Road cut consumer last fly knowledge. Material role treatment prove certainly case.</div>
```

### CompanyStats (all current records)

| ID | title | value | icon |
|---|---|---|---|
| 9 | American | 09+ | ph-globe |
| 10 | consumer | 55+ | ph-calendar |
| 11 | under | 29+ | ph-globe |
| 12 | yard | 74+ | ph-calendar |

### TeamMember (all current records)

Names are unverified/demo-looking; the audit does not establish that these are actual company employees. The repeated photograph depicts a hand holding a dandelion, not a portrait.

| ID | name | position | Placement |
|---|---|---|---|
| 31 | Benjamin Mcdonald | Theatre stage manager | Management |
| 32 | David Friedman | Retail manager | Management |
| 33 | Richard Wheeler | Dance movement psychotherapist | Management |
| 34 | James White | Multimedia programmer | Management |
| 35 | Mark Long | Publishing rights manager | Management |
| 36 | Colin Kennedy | Facilities manager | Staff |
| 37 | Jennifer Haynes MD | Arts administrator | Staff |
| 38 | Barbara Perez | Accountant, chartered | Staff |
| 39 | Gabrielle Kane | Health visitor | Staff |
| 40 | Jason Graham | Dealer | Staff |
| 41 | Erica Gray | Financial trader | Staff |
| 42 | Kimberly Spencer | Programmer, multimedia | Staff |
| 43 | Gina Rivera | Geographical information systems officer | Staff |
| 44 | Jeffrey Henry | Therapist, nutritional | Staff |
| 45 | Don Jones | Producer, television/film/video | Staff |

### FAQ (all current records)

**FAQ #11 — question:** Upon society from south focus alone.

**answer:** Strategy especially religious necessary he add. His pick even condition about company. Speak skill hair not risk. Economic PM among by describe stage cold.

**FAQ #12 — question:** Fly put establish politics head candidate.

**answer:** Bag there kind can. Evidence best value open space ability turn. Thus enough all job. Boy eye pass role whose. Father seem she around local rather.

**FAQ #13 — question:** Agent understand turn direction here.

**answer:** Bag how former social artist. Enter your by tonight reflect reduce feel. Rise fight three on success. Must at consider price son discover. Expect throughout attention new whole.

**FAQ #14 — question:** Or school third picture north hit home become card.

**answer:** Management success political wonder network course. Amount number modern my none court. Live agreement spend personal.

**FAQ #15 — question:** Policy north realize affect allow yard above others such door.

**answer:** Ability continue compare finish traditional yet write system. Wish role environmental defense on. Human law how window memory. Standard campaign subject key.

### Question topics requiring company answers

- Product categories and supported manufacturing capabilities.
- Minimum order quantities and how they vary by product.
- Sample development process, cost and timing.
- Production lead times and factors that affect scheduling.
- Verified capacity, units, and measurement period.
- Quality assurance, approved certifications and audit scope/validity.
- Export destinations, logistics and commercial terms.
- Responsible production and worker-welfare practices backed by evidence.
- How prospective customers submit specifications and request quotations.

These are editorial topics only, not claims or proposed answers.

## Admin usability and publication behavior

- AboutSection, TeamSection and FAQSection use the first record. They are not enforced singletons; superusers may add additional records that do not supply the page heading. Edit the existing #3 records rather than adding alternatives.
- About consumes CompanyStats.objects.all()[:4], shared with the homepage. CompanyStats has no order or visibility field and no explicit query ordering. Creating additional records is not a reliable way to choose the four published KPIs; update the existing four. Do not change query behavior as part of this audit.
- TeamMember.is_management selects management versus staff placement; it does not hide a person. There is no is_active/is_visible/publication checkbox. All records returned by the default manager are shown, regardless of section association. Do not use deletion as a reversible visibility control: the base model has HARD_DELETE_NOCASCADE policy.
- TeamMember.order controls ascending order within each group and is editable from the list. All current values tie at 0. Set distinct values when the approved roster is supplied.
- TeamMember.bio and email are editable but not displayed on About. linkedin_url is displayed only for management. The staff template does not render a LinkedIn link.
- FAQ entries are editable standalone and inline under FAQSection; question/answer/order are available. All entries returned by the default manager are displayed, irrespective of section assignment; there is no publication switch. Standalone FAQ answer uses the existing WYSIWYG widget.
- Site Settings General, Footer and Social Links tabs control the public brand copy and links. Legacy company_name/logo/footer_text fields are not the fields used by this About footer.
- About title, breadcrumb, section labels and CTA text are template copy. CTA destinations are named Django routes. Core values and footer contact details are not Admin-managed.

## Safe admin usability improvements recommended

No admin changes were necessary to complete this audit; these can be applied to ModelAdmin forms without schema changes:

- Label AboutSection.image “Hero and story image”; explain the dual crop and current 800×800 upload limit.
- Label TeamMember.position “Designation / job title” and is_management “Display in management group”; explain that false still publishes the member under staff.
- Add help text to order: “Lower values appear first; use distinct values.” Apply to both standalone and inline team/FAQ forms.
- Label CompanyStats.title “Metric label” and value “Verified display value”; request explicit units/time period and explain that About displays only four shared records.
- Add AboutSection/TeamSection/FAQSection form guidance to edit the existing record rather than adding another section.
- Add SiteSettings help text distinguishing public footer_description from legacy footer_text; clarify that footer phone/address/email are currently template-controlled.

Do not silently add visibility controls, change ordering rules, remove entries, change the image cap or wire new contact fields during this content audit. Those require scoped implementation decisions. No migrations are needed for form-only labels/help text.

## Verification

- Read current database records through Django ORM without saves/deletes.
- Inspected view selection rules, model fields, Admin fieldsets/inlines, templates and image optimizer.
- Read image dimensions and sizes; confirmed all 15 team image hashes match.
- Inspected the existing 1440×1080 version of the About photograph.
- Seeder factories use Faker for KPI labels/numbers, names/jobs and FAQ text, consistent with the demo data observed.
- External company facts, social profile ownership and contacts were not independently verified.
