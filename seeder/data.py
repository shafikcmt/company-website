"""Realistic demo content for Humana Apparels Ltd — a woven outerwear and
garment exporter in Gorai, Mirzapur (Tangail), Bangladesh.

Company facts (est. 1986, ~2,400 workers, 28 lines, 150,000 pcs/month, main
buyers, audit records) mirror the company's own compliance sheet. People,
testimonial authors and the fictional partner brands below are invented for
demo purposes; testimonials are never attributed to real brands.
"""

from datetime import date


SITE = {
    "site_name": "Humana Apparels Ltd",
    "site_tagline": "Woven outerwear, made responsibly since 1986",
    "header_cta_text": "Get in Touch",
    "header_cta_url": "/contact/",
    "footer_description": (
        "A 100% export-oriented garment manufacturer in Bangladesh, producing "
        "padded jackets, parkas and woven bottoms for brands across Europe and "
        "North America."
    ),
    "footer_address": "Gorai, Mirzapur, Tangail, Bangladesh",
    "footer_phone": "+880 2 5500 1986",
    "footer_email": "info@humanaapparels.com",
    "footer_links_title": "Quick Links",
    "footer_contact_title": "Get in Touch",
    "footer_social_title": "Follow Us",
    "footer_copyright": "© 2026 Humana Apparels Ltd. All rights reserved.",
    "meta_title": "Humana Apparels Ltd — Woven Outerwear Manufacturer in Bangladesh",
    "meta_description": (
        "Humana Apparels Ltd manufactures padded jackets, parkas and woven "
        "garments for global brands — BSCI, WRAP, GOTS and ISO 9001 certified."
    ),
}

HERO = {
    "badge_text": "Premier Garment Manufacturer",
    "title": "Outerwear crafted for the world's leading brands",
    "highlight_word": "crafted",
    "subtitle": (
        "From pattern to packed carton, our 28 production lines in Bangladesh "
        "deliver compliant, quality-assured woven garments on schedule."
    ),
    "cta_primary_text": "Explore Products",
    "cta_primary_url": "/products/",
    "cta_secondary_text": "Request a Quote",
    "cta_secondary_url": "/contact/",
    "bottom_label": "Humana Apparels Ltd",
    "bottom_link_text": "Inside our factory",
    "bottom_link_url": "/gallery/",
    "autoplay": True,
    "autoplay_interval": 6,
    "is_active": True,
}

HERO_SLIDES = [
    {"alt_text": "Operators at work on a sewing line in the Humana Apparels factory", "caption": "Sewing floor — 28 lines", "focal_point": "center", "label": "Sewing floor"},
    {"alt_text": "Quality inspector checking seams on a finished padded jacket", "caption": "Inline & final quality inspection", "focal_point": "center", "label": "Quality inspection"},
    {"alt_text": "Automated fabric cutting table with layered woven fabric", "caption": "Automated cutting room", "focal_point": "top", "label": "Cutting room"},
    {"alt_text": "Down-filling machines in the quilting section", "caption": "Down-filling & quilting", "focal_point": "center", "label": "Down-filling"},
    {"alt_text": "Finished jackets folded and packed in export cartons", "caption": "Packed for export", "focal_point": "bottom", "label": "Packing & export"},
    {"alt_text": "Pattern maker adjusting a jacket pattern on a design table", "caption": "Pattern & sampling studio", "focal_point": "center", "label": "Sampling studio"},
]

STATS_SECTION = {"title": "Humana Apparels in numbers", "subtitle": "Capacity and experience our buyers rely on"}
STATS = [
    {"icon": "ph-calendar-check", "number": 40, "suffix": "", "label": "Years of manufacturing since 1986"},
    {"icon": "ph-users-three", "number": 2400, "suffix": "+", "label": "Skilled workers on the floor"},
    {"icon": "ph-t-shirt", "number": 150, "suffix": "K", "label": "Garments produced every month"},
    {"icon": "ph-factory", "number": 28, "suffix": "", "label": "Fully equipped production lines"},
]

INTRO = {
    "eyebrow": "Who We Are",
    "title": "Crafting excellence in woven apparel",
    "subtitle": "A family-founded manufacturer that grew into a trusted outerwear partner.",
    "content": (
        "<p>Since 1986 Humana Apparels Ltd has specialised in technical woven "
        "garments — padded and down jackets, parkas, vests and trousers. Our "
        "219,000 sq ft facility in Gorai, Mirzapur combines automated cutting, "
        "down-filling and quilting with experienced sewing teams.</p>"
        "<p>Every order runs through documented quality checkpoints and an "
        "audited social-compliance system, so buyers get consistent product "
        "and full transparency.</p>"
    ),
    "cta_text": "Learn more about us",
    "cta_url": "/about/",
}
INTRO_FEATURES = [
    {"icon": "ph-stack", "title": "Full-package production", "description": "Sampling, sourcing, cutting, sewing, finishing and packing under one roof."},
    {"icon": "ph-seal-check", "title": "Certified & audited", "description": "BSCI, WRAP Gold, GOTS, GRS, OEKO-TEX® and ISO 9001:2015."},
    {"icon": "ph-truck", "title": "On-time delivery", "description": "Line planning and FOB Chattogram shipping built around your calendar."},
]

SERVICES_SECTION = {"eyebrow": "What We Offer", "title": "End-to-end garment manufacturing", "subtitle": "One partner from first sample to shipped carton."}
SERVICES = [
    {"icon": "ph-pen-nib", "title": "Product development & sampling", "description": "<p>Pattern making, proto, fit and salesman samples turned around in 7–10 days by our in-house sampling studio.</p>"},
    {"icon": "ph-scissors", "title": "Fabric & trims sourcing", "description": "<p>Nominated or self-sourced shell fabrics, recycled fills and certified trims with full traceability.</p>"},
    {"icon": "ph-needle", "title": "Cutting & sewing", "description": "<p>Automated cutting and 28 sewing lines configured for padded jackets, parkas and woven bottoms.</p>"},
    {"icon": "ph-feather", "title": "Down-filling & quilting", "description": "<p>Dedicated down-filling machines and computerised quilting for RDS-certified down and synthetic fills.</p>"},
    {"icon": "ph-magnifying-glass", "title": "Quality assurance", "description": "<p>Inline, pre-final and final AQL 2.5 inspections plus needle detection on every carton.</p>"},
    {"icon": "ph-package", "title": "Packing & logistics", "description": "<p>Buyer-specific packing, carton labelling and FOB or FCA shipment via Chattogram port.</p>"},
]

ABOUT = {
    "eyebrow": "Company Overview",
    "title": "Four decades of woven outerwear",
    "subtitle": "Built on craftsmanship, compliance and long-term partnerships.",
    "content": (
        "<p>Humana Apparels Ltd began as a small woven-garment unit in 1986. "
        "Today our team of 2,400 produces around 150,000 pieces a month for "
        "brands in Germany, France, the UK and the USA.</p>"
        "<p>We invest continuously in our people and our processes — from "
        "Better Work training programmes to energy-efficient machinery — "
        "because responsible manufacturing is how we earn repeat business.</p>"
    ),
    "banner_title": "About Us",
    "banner_subtitle": "The people, values and experience behind every garment we make.",
}

CORE_VALUES_SECTION = {"eyebrow": "What Drives Us", "title": "Our Core Values", "subtitle": "The principles behind every order we take on."}
CORE_VALUES = [
    {"icon": "ph-shield-check", "title": "Integrity", "description": "We operate transparently and ethically in every relationship and transaction."},
    {"icon": "ph-medal", "title": "Quality", "description": "Uncompromising standards from raw material to the finished garment."},
    {"icon": "ph-leaf", "title": "Sustainability", "description": "Responsible processes that protect the environment and future generations."},
    {"icon": "ph-users-three", "title": "People First", "description": "A safe, fair and empowering workplace for every member of our team."},
    {"icon": "ph-handshake", "title": "Reliability", "description": "On-time delivery and dependable partnerships our buyers can trust."},
    {"icon": "ph-lightbulb", "title": "Innovation", "description": "Continuously improving through technology and smarter ways of working."},
]

TEAM_SECTION = {"eyebrow": "Leadership", "title": "Meet our team", "subtitle": "Experienced people running a disciplined, transparent factory."}
MANAGEMENT = [
    {"name": "Rafiqul Islam", "position": "Managing Director"},
    {"name": "Nusrat Jahan", "position": "Director, Operations"},
    {"name": "Tanvir Ahmed", "position": "General Manager, Merchandising"},
    {"name": "Farhana Akter", "position": "Head of Compliance & HR"},
]
STAFF = [
    {"name": "Mahmudul Hasan", "position": "Senior Merchandiser"},
    {"name": "Sharmin Sultana", "position": "Quality Assurance Manager"},
    {"name": "Imran Hossain", "position": "Industrial Engineering Manager"},
    {"name": "Taslima Begum", "position": "Sampling Manager"},
    {"name": "Arif Chowdhury", "position": "Production Manager"},
    {"name": "Sabrina Rahman", "position": "Sustainability Officer"},
]

FAQ_SECTION = {"eyebrow": "Got Questions?", "title": "Frequently asked questions", "subtitle": "Quick answers for sourcing teams evaluating a new supplier."}
FAQS = [
    {"question": "What products do you specialise in?", "answer": "<p>Woven outerwear — padded and down jackets, parkas, vests and quilted styles — plus woven trousers and shirts for men, women and kids.</p>"},
    {"question": "What is your minimum order quantity?", "answer": "<p>Typically 1,000 pieces per style, split across up to four colourways. Smaller development orders can be discussed for new programmes.</p>"},
    {"question": "What are your production lead times?", "answer": "<p>60–90 days from approved PP sample and fabric in-house, depending on construction and fill type.</p>"},
    {"question": "Which certifications do you hold?", "answer": "<p>BSCI, WRAP (Gold), GOTS, OCS, RCS, GRS, RDS, OEKO-TEX® Standard 100, Higg FEM verification and ISO 9001:2015, among others. See the Compliance page for current status.</p>"},
    {"question": "Do you offer sampling and product development?", "answer": "<p>Yes. Our in-house studio handles pattern making, proto, fit, size-set and salesman samples.</p>"},
    {"question": "What are your shipping terms?", "answer": "<p>We usually ship FOB Chattogram; FCA and CIF can be arranged on request.</p>"},
]

CUSTOMERS_PAGE = {
    "eyebrow": "Trusted By",
    "title": "Our valued buyers",
    "subtitle": "Brands across Europe and North America that trust us with their outerwear programmes.",
    "banner_title": "Our Customers",
    "banner_subtitle": "Long-term partnerships built on quality, compliance and on-time delivery.",
}
# Real main buyers from the company's compliance sheet, plus fictional demo brands.
CUSTOMERS = [
    {"name": "Hugo Boss", "url": "https://www.hugoboss.com", "is_featured": True},
    {"name": "Marco Polo", "url": "https://example.com/marco-polo", "is_featured": True},
    {"name": "Macy's", "url": "https://www.macys.com", "is_featured": True},
    {"name": "Antailor", "url": "https://example.com/antailor", "is_featured": True},
    {"name": "Nordic Outdoor Co.", "url": "https://example.com/nordic-outdoor", "is_featured": True},
    {"name": "Atlantic Workwear", "url": "https://example.com/atlantic-workwear", "is_featured": True},
    {"name": "Alpine Trail Apparel", "url": "https://example.com/alpine-trail", "is_featured": False},
    {"name": "Harbour & Pine", "url": "https://example.com/harbour-pine", "is_featured": False},
    {"name": "Meridian Kids", "url": "https://example.com/meridian-kids", "is_featured": False},
    {"name": "Fjell Sport", "url": "https://example.com/fjell-sport", "is_featured": False},
]

TESTIMONIALS_SECTION = {"eyebrow": "Kind Words", "title": "What our partners say", "subtitle": "Feedback from sourcing and quality teams we work with."}
# Fictional people at fictional brands — never attributed to real buyers.
TESTIMONIALS = [
    {"author": "Lena Hoffmann", "position": "Head of Sourcing, Nordic Outdoor Co.", "is_featured": True,
     "content": "Humana has delivered our core down-jacket programme for five seasons running. Fit consistency and on-time shipment have been excellent, and their compliance documentation is always audit-ready."},
    {"author": "James Whitfield", "position": "Technical Manager, Atlantic Workwear", "is_featured": False,
     "content": "Their sampling team turns comments around in days, not weeks. The quilting quality on our padded vests is the best we have seen in the region."},
    {"author": "Claire Dubois", "position": "Quality Lead, Harbour & Pine", "is_featured": False,
     "content": "Final inspection pass rates are consistently high and their QA team flags issues before they become problems. A very transparent partner."},
    {"author": "Mikkel Sørensen", "position": "Production Director, Fjell Sport", "is_featured": False,
     "content": "We moved our recycled-fill parkas to Humana for their GRS certification and traceability. The transition was smooth and well documented."},
]

ACTIVITIES_PAGE = {
    "eyebrow": "News & Activities",
    "title": "Our Activities",
    "subtitle": "CSR, compliance and community initiatives from across Humana Apparels.",
    "banner_title": "News & Activities",
    "banner_subtitle": "Audits, certifications, training and community work from our factory floor.",
}
ACTIVITIES = [
    {"tag": "Compliance", "title": "BSCI social audit completed successfully", "is_featured": True, "activity_date": date(2026, 6, 2),
     "excerpt": "Our facility in Gorai, Mirzapur completed its latest amfori BSCI social compliance audit, reaffirming our commitment to ethical labour practices."},
    {"tag": "Sustainability", "title": "GOTS-certified organic cotton line launched", "is_featured": True, "activity_date": date(2026, 5, 15),
     "excerpt": "A new GOTS-certified organic cotton line expands our capability and supports our partner brands' sustainability goals."},
    {"tag": "Community", "title": "Worker welfare training programme", "is_featured": True, "activity_date": date(2026, 4, 21),
     "excerpt": "Ongoing skills and welfare sessions for our workforce under the Better Work programme, covering rights, health and career growth."},
    {"tag": "Safety", "title": "Annual fire-safety drill with RSC observers", "is_featured": False, "activity_date": date(2026, 3, 10),
     "excerpt": "All three shifts completed a full evacuation drill in under four minutes, observed by RSC safety engineers."},
    {"tag": "Quality", "title": "ISO 9001:2015 quality certification achieved", "is_featured": False, "activity_date": date(2026, 2, 3),
     "excerpt": "Our quality management system was certified to ISO 9001:2015 following a two-stage external audit."},
    {"tag": "CSR", "title": "Free health camp for workers and families", "is_featured": False, "activity_date": date(2026, 1, 18),
     "excerpt": "More than 600 workers and family members received free check-ups, eye tests and medicines at our on-site health camp."},
]

CAREER_PAGE = {
    "eyebrow": "Careers",
    "title": "Career Opportunities",
    "subtitle": "Join a team of 2,400 people making garments for the world's leading brands.",
    "banner_title": "Build your career with us",
    "banner_subtitle": "Join a team of 2,400 people making garments for the world's leading brands.",
    "positions_title": "Open Positions",
    "positions_empty_text": "There are no open positions at the moment. Please check back later.",
}
POSITIONS = [
    {"title": "Senior Merchandiser — Woven Outerwear", "department": "Merchandising", "location": "Dhaka (Head Office)", "type": "Full-time", "job_type": "full-time",
     "description": "<p>Own buyer communication, costing and sample approvals for two European outerwear accounts.</p><ul><li>5+ years in woven / padded jacket merchandising</li><li>Strong costing and T&amp;A planning skills</li></ul>"},
    {"title": "Quality Assurance Executive", "department": "Quality", "location": "Gorai, Mirzapur (Factory)", "type": "Full-time", "job_type": "full-time",
     "description": "<p>Run inline and final AQL inspections and lead root-cause analysis with production teams.</p><ul><li>Diploma or B.Sc. in Textile Engineering</li><li>2+ years of QA experience in outerwear</li></ul>"},
    {"title": "Industrial Engineer", "department": "Industrial Engineering", "location": "Gorai, Mirzapur (Factory)", "type": "Full-time", "job_type": "full-time",
     "description": "<p>Balance lines, set SMVs and drive efficiency improvements across 28 sewing lines.</p><ul><li>B.Sc. in Industrial / Textile Engineering</li><li>Experience with GSD or similar</li></ul>"},
    {"title": "Compliance Officer", "department": "Compliance & HR", "location": "Gorai, Mirzapur (Factory)", "type": "Full-time", "job_type": "full-time",
     "description": "<p>Maintain audit readiness for BSCI, WRAP and buyer codes of conduct, and coordinate corrective actions.</p><ul><li>3+ years in social compliance</li><li>Knowledge of Bangladesh Labour Act</li></ul>"},
]

CONTACT_PAGE = {
    "eyebrow": "Contact",
    "title": "Contact Us",
    "subtitle": "Talk to our merchandising team about your next programme.",
    "banner_title": "Let's talk",
    "banner_subtitle": "Tell us about your product and our merchandising team will get back to you within one business day.",
    "groups_title": "Key Contacts",
    "groups_empty_text": "We'd love to hear from you — reach us using the details on the left.",
    "socials_title": "Connect With Us",
}
CONTACT_DATA = {
    "office_title": "Factory & Office",
    "office_subtitle": "Visit us or reach out — we reply within one business day.",
    "address": "Gorai, Mirzapur, Tangail, Bangladesh",
    "fax": "+880 2 5500 1987",
    "map_title": "Find us",
    "map_subtitle": "Our factory is on the Dhaka–Tangail highway at Gorai, Mirzapur.",
    "map_url": "https://www.google.com/maps?q=Gorai,+Mirzapur,+Tangail&output=embed",
}
CONTACT_PHONES = [
    {"number": "+880 2 5500 1986", "type": "phone", "is_primary": True},
    {"number": "+880 1711 001986", "type": "whatsapp", "is_primary": False},
]
CONTACT_EMAILS = [
    {"email": "info@humanaapparels.com", "department": "General", "is_primary": True},
    {"email": "merchandising@humanaapparels.com", "department": "Merchandising", "is_primary": False},
    {"email": "careers@humanaapparels.com", "department": "Careers", "is_primary": False},
]
CONTACT_GROUPS = {
    "Merchandising": [
        {"name": "Tanvir Ahmed", "position": "General Manager, Merchandising", "email": "tanvir@humanaapparels.com", "phone": "+8801711002001"},
        {"name": "Mahmudul Hasan", "position": "Senior Merchandiser", "email": "mahmudul@humanaapparels.com", "phone": "+8801711002002"},
    ],
    "Compliance & HR": [
        {"name": "Farhana Akter", "position": "Head of Compliance & HR", "email": "farhana@humanaapparels.com", "phone": "+8801711002003"},
        {"name": "Sabrina Rahman", "position": "Sustainability Officer", "email": "sabrina@humanaapparels.com", "phone": "+8801711002004"},
    ],
}
SOCIALS = [
    {"name": "LinkedIn", "url": "https://www.linkedin.com/company/humana-apparels", "icon": "ph-linkedin-logo"},
    {"name": "Facebook", "url": "https://www.facebook.com/humanaapparels", "icon": "ph-facebook-logo"},
    {"name": "YouTube", "url": "https://www.youtube.com/@humanaapparels", "icon": "ph-youtube-logo"},
]

PRODUCTS_PAGE = {
    "eyebrow": "Products",
    "title": "Our Products",
    "subtitle": "Woven outerwear and bottoms for men, women and kids.",
    "banner_title": "Our Products",
    "banner_subtitle": "Padded jackets, parkas, vests and woven bottoms — engineered, sampled and produced in-house.",
    "portfolio_eyebrow": "What We Make",
    "portfolio_title": "Product portfolio",
    "portfolio_subtitle": "A selection of styles produced for our buyers.",
    "cta_title": "Looking for a manufacturing partner?",
    "cta_text": "Tell us about your product and we'll show you what Humana Apparels can deliver.",
    "cta_button_text": "Request a quote",
    "cta_button_url": "/contact/",
}
PRODUCT_CAROUSEL = ["Padded jackets", "Parkas", "Quilted vests"]
PRODUCT_SECTIONS = [
    {"eyebrow": "Capabilities", "title": "Outerwear specialists", "after_products": False,
     "description": "<p>Padded and down jackets are our core. Multi-panel constructions, taped seams and two-way zips are everyday work for our lines.</p>"},
    {"eyebrow": "Capabilities", "title": "Down & quilting expertise", "after_products": False,
     "description": "<p>Dedicated down-filling machines and computerised quilting deliver even fill distribution with RDS-certified down or recycled synthetic fills.</p>"},
    {"eyebrow": "Development", "title": "Sampling in 7–10 days", "after_products": True,
     "description": "<p>Our sampling studio works from your tech pack to deliver proto, fit and salesman samples fast, with pattern corrections handled in-house.</p>"},
]
PRODUCT_CATEGORIES = {
    "Jackets": [
        ("Men's Hooded Down Jacket", "Male", "Hugo Boss"),
        ("Men's Lightweight Padded Jacket", "Male", "Marco Polo"),
        ("Women's Quilted Puffer Jacket", "Female", "Macy's"),
        ("Women's Belted Down Coat", "Female", "Antailor"),
        ("Men's Packable Travel Jacket", "Male", "Nordic Outdoor Co."),
        ("Women's Cropped Puffer", "Female", "Harbour & Pine"),
    ],
    "Parkas": [
        ("Men's Fishtail Parka", "Male", "Hugo Boss"),
        ("Women's Faux-Fur Hood Parka", "Female", "Macy's"),
        ("Men's Waterproof Utility Parka", "Male", "Atlantic Workwear"),
        ("Women's Long Recycled-Fill Parka", "Female", "Fjell Sport"),
    ],
    "Vests": [
        ("Men's Quilted Gilet", "Male", "Marco Polo"),
        ("Women's Down Vest", "Female", "Antailor"),
        ("Kids' Padded Vest", None, "Meridian Kids"),
    ],
    "Trousers": [
        ("Men's Stretch Chino", "Male", "Hugo Boss"),
        ("Men's Cargo Trousers", "Male", "Atlantic Workwear"),
        ("Women's Wide-Leg Trousers", "Female", "Harbour & Pine"),
    ],
}

COMPLIANCE_PAGE = {
    "eyebrow": "Compliance Documentation",
    "title": "Compliance",
    "subtitle": "Our commitment to ethical and safe manufacturing.",
    "banner_title": "Our Compliance & Certifications",
    "banner_subtitle": "Committed to global standards in social, environmental and quality compliance.",
    "audit_eyebrow": "Accredited & Audited",
    "audit_title": "Audit Status",
    "audit_description": "Current status of all social, environmental, security and quality certifications held by Humana Apparels Ltd.",
    "standards_title": "Standards & Code of Conduct",
    "standards_description": "The frameworks and practices we are held accountable to, documented for review.",
    "certificates_eyebrow": "Accredited & Audited",
    "certificates_title": "Our Certifications",
    "cta_title": "Need our compliance documentation?",
    "cta_text": "Request audit reports, certification copies or any compliance-related details from our team.",
    "cta_button_text": "Request Documentation",
    "cta_button_url": "/contact/",
}
COMPLIANCE_SECTIONS = [
    {"eyebrow": "Social", "title": "Social compliance (amfori BSCI & WRAP)", "description": "<p>Fair wages, regulated working hours, freedom of association and zero tolerance for child or forced labour — independently audited every cycle.</p>"},
    {"eyebrow": "Safety", "title": "Building, fire & electrical safety (RSC)", "description": "<p>Structural, fire and electrical safety is monitored under the RMG Sustainability Council, with remediation tracked to closure.</p>"},
    {"eyebrow": "Environment", "title": "Environmental management (Higg FEM)", "description": "<p>Energy, water, waste and chemicals are measured and verified through the Higg Facility Environmental Module.</p>"},
    {"eyebrow": "Security", "title": "Supply-chain security (C-TPAT)", "description": "<p>Controlled access, container sealing and cargo security procedures meet C-TPAT requirements for US-bound shipments.</p>"},
    {"eyebrow": "Quality", "title": "Quality management (ISO 9001:2015)", "description": "<p>A certified quality management system governs every step from fabric inspection to final AQL audit.</p>"},
]
COMPLIANCE_CERTIFICATES = [
    ("amfori BSCI", "https://www.amfori.org"),
    ("WRAP", "https://wrapcompliance.org"),
    ("GOTS", "https://global-standard.org"),
    ("OCS", "https://textileexchange.org"),
    ("RCS", "https://textileexchange.org"),
    ("GRS", "https://textileexchange.org"),
    ("RDS", "https://textileexchange.org"),
    ("OEKO-TEX Standard 100", "https://www.oeko-tex.com"),
    ("ISO 9001:2015", "https://www.iso.org"),
    ("Higg FEM", "https://howtohigg.org"),
]

SUSTAINABILITY_PAGE = {
    "eyebrow": "Our Sustainability Journey",
    "title": "Sustainability",
    "subtitle": "Our initiatives for a greener and more responsible future.",
    "banner_title": "Manufacturing with the planet in mind.",
    "banner_subtitle": "From cleaner production to responsible sourcing, every step we take is a commitment to lighter footprints and brighter communities.",
    "certificates_title": "Recognized By",
    "cta_title": "Let's build a greener supply chain.",
    "cta_text": "Partner with a manufacturer that treats sustainability as a journey, not a checkbox.",
    "cta_button_text": "Start the Conversation",
    "cta_button_url": "/contact/",
}
SUSTAINABILITY_SECTIONS = [
    {"title": "Cleaner production", "description": "<p>LED lighting, servo-motor sewing machines and compressed-air leak programmes have cut our electricity use per garment year on year.</p>"},
    {"title": "Responsible materials", "description": "<p>GOTS organic cotton, GRS recycled polyester and RDS down let our buyers trace materials from source to finished product.</p>"},
    {"title": "Water & waste stewardship", "description": "<p>Rainwater harvesting, metered water use and segregated waste streams — with fabric off-cuts sent for recycling instead of landfill.</p>"},
    {"title": "People & community", "description": "<p>Health camps, skills training and Better Work programmes support our workers and the communities around our factory.</p>"},
]
SUSTAINABILITY_CERTIFICATES = ["GOTS", "GRS", "RCS", "OCS", "RDS", "Regenagri"]

GALLERY_PAGE = {
    "eyebrow": "Gallery",
    "title": "Gallery",
    "subtitle": "Inside our factory, our products and our people.",
    "banner_title": "Inside Humana Apparels",
    "banner_subtitle": "A look at our factory floor, our products and the people who make them.",
    "all_tab_label": "All",
    "videos_title": "Videos",
}
GALLERY_SECTIONS = {
    "Production": ["Cutting room", "Sewing line", "Down-filling section", "Quilting machines", "Finishing table", "Pressing section"],
    "Quality Control": ["Fabric inspection", "Inline inspection", "Needle detection", "Final AQL audit"],
    "People": ["Morning briefing", "Skills training", "Sampling team", "Merchandising team"],
    "Events": ["Health camp", "Fire-safety drill", "Annual sports day", "Buyer visit"],
}
