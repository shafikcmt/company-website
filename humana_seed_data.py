"""
Humana Apparels Ltd — Complete Seed Data
explore-bd.com images + Humana Apparels content

Run: python manage.py shell < humana_seed_data.py
OR copy into seeder/management/commands/seed_content.py
"""

import requests
import os
from django.core.files.base import ContentFile
from hapl.models import (
    HomeHeroSection, HomeCarouselSlide,
    HomeIntroductionSection, HomeIntroductionFeature,
    HomeServicesSection, Service,
    HomeStatsSection, CompanyStats,
    AboutSection,
    TeamSection, TeamMember,
    FAQSection, FAQ,
    CustomersSection, Customer,
    TestimonialsSection, Testimonial,
    ActivitiesSection, Activity,
    ProductsPage, ProductCarouselSlide, ProductSection,
    ProductCategory, Product,
    CompliancePage, ComplianceSection, ComplianceCertificate,
    SustainabilityPage, SustainabilitySection, SustainabilityCertificate,
    GalleryPage, GallerySection, GalleryImage,
    ContactSection, ContactData, ContactPhone, ContactEmail,
    ContactGroup, ContactMember, Social,
    CareerSection, CareerPosition,
)


def download_image(url):
    """Download image from URL and return ContentFile"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            filename = url.split('/')[-1]
            return ContentFile(response.content, name=filename)
    except Exception as e:
        print(f"  ⚠️ Could not download {url}: {e}")
    return None


def seed_hero():
    print("🎠 Seeding Hero Carousel...")
    section, _ = HomeHeroSection.objects.get_or_create(id=1)

    slides_data = [
        {
            "title": "Crafting Excellence, Dressing the World",
            "subtitle": "Humana Apparels Ltd is a 100% export-oriented woven garment manufacturer based in Bangladesh, trusted by 120+ global buyers across USA, UK, Germany, France and beyond.",
            "image_url": "https://explore-bd.com/wp-content/uploads/2025/06/1-16.png",
            "cta_text": "Explore Products",
            "cta_url": "/products/",
        },
        {
            "title": "Quality Woven Garments for Global Markets",
            "subtitle": "From state-of-the-art manufacturing facilities to stringent quality control, we deliver world-class apparel that meets the highest international standards.",
            "image_url": "https://explore-bd.com/wp-content/uploads/2025/06/2-15.png",
            "cta_text": "About Us",
            "cta_url": "/about/",
        },
        {
            "title": "Sustainable Fashion Manufacturing",
            "subtitle": "Committed to eco-friendly production practices, LEED certified facility, and internationally recognized compliance standards for a better tomorrow.",
            "image_url": "https://explore-bd.com/wp-content/uploads/2025/06/3-15.png",
            "cta_text": "Our Compliance",
            "cta_url": "/compliance/",
        },
        {
            "title": "Your Trusted Garment Partner in Bangladesh",
            "subtitle": "With over 15 years of experience and a dedicated workforce of 5,000+ skilled workers, we bring your fashion vision to life with precision and care.",
            "image_url": "https://explore-bd.com/wp-content/uploads/2025/06/4-8.png",
            "cta_text": "Contact Us",
            "cta_url": "/contact/",
        },
        {
            "title": "World-Class Facilities, Global Standards",
            "subtitle": "Our modern factory spans 500,000+ sq ft with cutting-edge machinery, dedicated QC labs, and a team committed to on-time delivery every time.",
            "image_url": "https://explore-bd.com/wp-content/uploads/2025/06/5-4.png",
            "cta_text": "View Gallery",
            "cta_url": "/gallery/",
        },
        {
            "title": "Mens & Ladies Wear Specialists",
            "subtitle": "Specializing in high-quality woven garments — shirts, trousers, jackets, dresses — for leading international fashion brands and retailers worldwide.",
            "image_url": "https://explore-bd.com/wp-content/uploads/2025/06/6-2.png",
            "cta_text": "Our Products",
            "cta_url": "/products/",
        },
    ]

    HomeCarouselSlide.objects.filter(section=section).delete()
    for i, data in enumerate(slides_data):
        slide = HomeCarouselSlide(
            section=section,
            title=data["title"],
            subtitle=data["subtitle"],
            cta_text=data["cta_text"],
            cta_url=data["cta_url"],
            is_active=True,
        )
        img = download_image(data["image_url"])
        if img:
            slide.image.save(img.name, img, save=False)
        slide.save()
        print(f"  ✅ Slide {i+1}: {data['title'][:40]}...")

    print(f"  ✅ Hero: {len(slides_data)} slides created\n")


def seed_introduction():
    print("📖 Seeding Introduction Section...")
    intro, _ = HomeIntroductionSection.objects.get_or_create(id=1)
    intro.title = "About Humana Apparels Ltd"
    intro.subtitle = "A Premier Garment Manufacturer from Bangladesh"
    intro.content = """Humana Apparels Ltd. is a prominent name in the global textile industry, specializing in the production of high-quality woven garments. Established in 2008, our state-of-the-art factory spans over 500,000 square feet with 10 production floors.

As a 100% export-oriented manufacturing facility, Humana Apparels has rapidly become a key player in supplying premium garments to the USA, Canada, the UK, Germany, France, Italy, Spain, Poland, Japan, Korea, and Brazil, among other international markets.

Our commitment to quality, compliance, and sustainability has earned us the trust of over 120 global buyers and recognition as one of Bangladesh's leading garment manufacturers."""

    img = download_image("https://explore-bd.com/wp-content/uploads/2025/06/denim-statement.webp")
    if img:
        intro.image.save(img.name, img, save=False)
    intro.save()

    features_data = [
        ("factory", "500,000+ Sq Ft Factory", "State-of-the-art manufacturing facility with modern machinery and technology"),
        ("users", "5,000+ Skilled Workers", "A dedicated and trained workforce ensuring precision in every garment"),
        ("globe", "120+ Global Buyers", "Trusted by leading international fashion brands across 25+ countries"),
        ("certificate", "Fully Compliance Certified", "LEED, BSCI, ISO and all major international compliance certifications"),
    ]

    HomeIntroductionFeature.objects.filter(introduction=intro).delete()
    for icon, title, desc in features_data:
        HomeIntroductionFeature.objects.create(
            introduction=intro, icon=icon, title=title, description=desc
        )
    print(f"  ✅ Introduction + {len(features_data)} features created\n")


def seed_stats():
    print("📊 Seeding Stats...")
    section, _ = HomeStatsSection.objects.get_or_create(id=1)
    section.title = "Humana Apparels by the Numbers"
    section.subtitle = "Our growth reflects our commitment to excellence"
    section.save()

    CompanyStats.objects.filter(section=section).delete()
    stats = [
        ("Workers", "5,000+", "users"),
        ("Global Buyers", "120+", "briefcase"),
        ("Export Countries", "25+", "globe"),
        ("Years Experience", "15+", "calendar"),
    ]
    for title, value, icon in stats:
        CompanyStats.objects.create(section=section, title=title, value=value, icon=icon)
    print(f"  ✅ Stats: {len(stats)} items\n")


def seed_services():
    print("⚙️ Seeding Services / Training Section...")
    section, _ = HomeServicesSection.objects.get_or_create(id=1)
    section.title = "Training & Development"
    section.subtitle = "Investing in our people for world-class manufacturing"
    section.save()

    Service.objects.filter(section=section).delete()
    services = [
        ("production", "Production Training", "Comprehensive training programs to enhance production efficiency, quality output and technical skills of our workforce."),
        ("shield", "Safety & Compliance", "Regular training on fire safety, PPE, emergency procedures and health & safety standards for all employees."),
        ("heart", "Worker Welfare", "HR manual training, capacity building, and awareness programs ensuring internationally acceptable working conditions."),
        ("chart-bar", "Quality Assurance", "Rigorous QC training at every production stage — from fabric inspection to final shipment — ensuring zero defect delivery."),
        ("leaf", "Sustainability", "Environmental awareness and green manufacturing practices integrated into daily operations across all departments."),
        ("users", "Leadership Development", "Management and supervisory skill development programs to build the next generation of garment industry leaders."),
    ]
    for icon, title, desc in services:
        Service.objects.create(section=section, icon=icon, title=title, description=desc)
    print(f"  ✅ Services: {len(services)} items\n")


def seed_products():
    print("👔 Seeding Products...")
    page, _ = ProductsPage.objects.get_or_create(id=1)
    page.title = "Our Products"
    page.subtitle = "Premium woven garments crafted for global fashion markets"
    page.save()

    # Mens Wear Category
    mens_cat, _ = ProductCategory.objects.get_or_create(page=page, name="Mens Wear")
    mens_images = [
        "https://explore-bd.com/wp-content/uploads/2025/06/1-1.webp",
        "https://explore-bd.com/wp-content/uploads/2025/06/2-6.jpg",
        "https://explore-bd.com/wp-content/uploads/2025/06/3-2.webp",
        "https://explore-bd.com/wp-content/uploads/2025/06/4-1.webp",
        "https://explore-bd.com/wp-content/uploads/2025/06/5-3.jpg",
        "https://explore-bd.com/wp-content/uploads/2025/06/6-3.jpg",
    ]
    mens_names = ["Woven Shirt", "Denim Jacket", "Cargo Trousers", "Formal Shirt", "Chino Pants", "Casual Jacket"]
    buyers = ["H&M", "Zara", "Next", "Primark", "C&A", "Lidl"]

    Product.objects.filter(category=mens_cat).delete()
    for i, (img_url, name, buyer) in enumerate(zip(mens_images, mens_names, buyers)):
        product = Product(category=mens_cat, name=name, buyer=buyer, gender="Male")
        img = download_image(img_url)
        if img:
            product.image.save(img.name, img, save=False)
        product.save()
        print(f"  ✅ Mens: {name}")

    # Ladies Wear Category
    ladies_cat, _ = ProductCategory.objects.get_or_create(page=page, name="Ladies Wear")
    ladies_images = [
        "https://explore-bd.com/wp-content/uploads/2025/06/5-1.webp",
        "https://explore-bd.com/wp-content/uploads/2025/06/4.webp",
        "https://explore-bd.com/wp-content/uploads/2025/06/3-6.jpg",
        "https://explore-bd.com/wp-content/uploads/2025/06/1-3.jpg",
    ]
    ladies_names = ["Ladies Blouse", "Woven Dress", "Casual Top", "Fashion Shirt"]
    ladies_buyers = ["Mango", "Esprit", "Tom Tailor", "Marks & Spencer"]

    Product.objects.filter(category=ladies_cat).delete()
    for i, (img_url, name, buyer) in enumerate(zip(ladies_images, ladies_names, ladies_buyers)):
        product = Product(category=ladies_cat, name=name, buyer=buyer, gender="Female")
        img = download_image(img_url)
        if img:
            product.image.save(img.name, img, save=False)
        product.save()
        print(f"  ✅ Ladies: {name}")

    print()


def seed_gallery():
    print("🖼️ Seeding Gallery...")
    page, _ = GalleryPage.objects.get_or_create(id=1)
    page.title = "Our Factory Gallery"
    page.subtitle = "A glimpse inside Humana Apparels Ltd"
    page.save()

    factory_section, _ = GallerySection.objects.get_or_create(page=page, name="Factory")

    gallery_images = [
        ("https://explore-bd.com/wp-content/uploads/2025/06/1-Factory-Front-View.jpeg", "Factory Front View"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/2-Guest-House.jpeg", "Guest House"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/3-Internal-Fire-Drill-Assembly-point.jpeg", "Internal Fire Drill"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/4-Training-Development.jpg", "Training & Development"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/4-Child-Care-Zone-scaled.jpg", "Child Care Zone"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/5-Factory-Dining-Hall-scaled.jpg", "Factory Dining Hall"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/6-Factory-at-a-Glance.jpeg", "Factory at a Glance"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/8-705-kW-solar-power-system.jpeg", "705 kW Solar Power System"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/7-Factory-Security-Guard-scaled.jpg", "Factory Security"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/9-Medical-Centre.jpeg", "Medical Centre"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/10-Feeding-Area-scaled.jpg", "Feeding Area"),
        ("https://explore-bd.com/wp-content/uploads/2025/06/11-Fire-Protection-scaled.jpg", "Fire Protection"),
    ]

    GalleryImage.objects.filter(section=factory_section).delete()
    for url, caption in gallery_images:
        gi = GalleryImage(section=factory_section, caption=caption)
        img = download_image(url)
        if img:
            gi.image.save(img.name, img, save=False)
        gi.save()
        print(f"  ✅ Gallery: {caption}")

    print()


def seed_about():
    print("🏭 Seeding About Section...")
    about, _ = AboutSection.objects.get_or_create(id=1)
    about.title = "About Humana Apparels Ltd"
    about.subtitle = "Bangladesh's Trusted Garment Manufacturing Partner"
    about.content = """Humana Apparels Ltd. is a leading name in Bangladesh's garment export industry, specializing in premium woven garments for the global fashion market. Founded with a vision to deliver world-class apparel, we have grown into a state-of-the-art manufacturing powerhouse over the past 15+ years.

Our modern facility spans over 500,000 square feet across multiple production floors, equipped with the latest machinery and technology. We employ over 5,000 skilled workers who are trained to the highest international standards.

As a 100% export-oriented company, we supply to leading international fashion brands in the USA, Canada, UK, Germany, France, Italy, Spain, Poland, Japan, Korea, Brazil and many more markets. Our commitment to quality, compliance, and timely delivery has made us a preferred manufacturing partner for global buyers.

We hold certifications in BSCI, ISO 9001, OEKO-TEX, and are a LEED-certified green factory — a testament to our dedication to sustainable and responsible manufacturing."""

    img = download_image("https://explore-bd.com/wp-content/uploads/2024/12/vision-e-mission.jpg")
    if img:
        about.image.save(img.name, img, save=False)
    about.save()
    print("  ✅ About section created\n")


def seed_activities():
    print("🤝 Seeding Activities...")
    section, _ = ActivitiesSection.objects.get_or_create(id=1)
    section.title = "Our Activities"
    section.subtitle = "CSR, compliance and community initiatives from across Humana Apparels"
    section.save()

    Activity.objects.all().delete()
    activities = [
        {
            "tag": "Compliance",
            "title": "BSCI Social Audit Completed Successfully",
            "excerpt": "Our facility in Gorai, Mirzapur successfully completed its latest BSCI social compliance audit, reaffirming our commitment to ethical labor practices.",
            "is_featured": True,
            "image_url": "https://explore-bd.com/wp-content/uploads/2025/06/3-Internal-Fire-Drill-Assembly-point.jpeg",
        },
        {
            "tag": "Sustainability",
            "title": "GOTS-Certified Organic Cotton Line Launched",
            "excerpt": "We've expanded our production capability with a new GOTS-certified organic cotton line, supporting our partner brands' sustainability goals.",
            "is_featured": True,
            "image_url": "https://explore-bd.com/wp-content/uploads/2025/06/8-705-kW-solar-power-system.jpeg",
        },
        {
            "tag": "Community",
            "title": "Worker Welfare Training Program",
            "excerpt": "Ongoing skills and welfare training sessions for our workforce, reflecting our commitment to worker development under the Better Work program.",
            "is_featured": True,
            "image_url": "https://explore-bd.com/wp-content/uploads/2025/06/4-Child-Care-Zone-scaled.jpg",
        },
    ]

    import datetime
    for i, data in enumerate(activities):
        activity = Activity(
            section=section,
            title=data["title"],
            excerpt=data["excerpt"],
            tag=data["tag"],
            is_featured=data["is_featured"],
            activity_date=datetime.date.today(),
        )
        img = download_image(data["image_url"])
        if img:
            activity.image.save(img.name, img, save=False)
        activity.save()
        print(f"  ✅ Activity: {data['title'][:50]}...")
    print()


def seed_contact():
    print("📞 Seeding Contact...")
    section, _ = ContactSection.objects.get_or_create(id=1)
    section.title = "Contact Us"
    section.subtitle = "Get in touch with our team for inquiries, samples, or partnership discussions"
    section.save()

    data, _ = ContactData.objects.get_or_create(section=section)
    data.map_title = "Find Our Factory"
    data.map_subtitle = "Located in the heart of Bangladesh's garment hub"
    data.map_url = "https://maps.google.com/?q=Dhaka,Bangladesh"
    data.address = "123 Garment Industrial Area, Ashulia, Savar, Dhaka-1340, Bangladesh"
    data.office_title = "Our Office"
    data.office_subtitle = "Visit us or reach out through any channel"
    data.fax = "+880-2-XXXXXXXX"

    img = download_image("https://explore-bd.com/wp-content/uploads/2025/06/1-Factory-Front-View.jpeg")
    if img:
        data.office_image.save(img.name, img, save=False)
        data.map_image.save("map_" + img.name, img, save=False)
    data.save()

    ContactPhone.objects.filter(contact=data).delete()
    ContactPhone.objects.create(contact=data, number="+880-XXXX-XXXXXX", type="phone", is_primary=True)
    ContactPhone.objects.create(contact=data, number="+880-XXXX-XXXXXX", type="whatsapp", is_primary=True)

    ContactEmail.objects.filter(contact=data).delete()
    ContactEmail.objects.create(contact=data, email="sales@humanaapparels.com", department="Sales", is_primary=True)
    ContactEmail.objects.create(contact=data, email="info@humanaapparels.com", department="General", is_primary=False)
    ContactEmail.objects.create(contact=data, email="compliance@humanaapparels.com", department="Compliance", is_primary=False)

    Social.objects.filter(section=section).delete()
    socials = [
        ("Facebook", "https://www.facebook.com/humanaapparels", "ph-facebook-logo"),
        ("LinkedIn", "https://www.linkedin.com/company/humana-apparels", "ph-linkedin-logo"),
        ("YouTube", "https://www.youtube.com/@humanaapparels", "ph-youtube-logo"),
        ("Instagram", "https://www.instagram.com/humanaapparels", "ph-instagram-logo"),
    ]
    for name, url, icon in socials:
        Social.objects.create(section=section, name=name, url=url, icon=icon)

    print("  ✅ Contact data created\n")


def seed_career():
    print("💼 Seeding Career...")
    section, _ = CareerSection.objects.get_or_create(id=1)
    section.title = "Career Opportunities"
    section.subtitle = "Join the Humana Apparels family and grow with us"
    section.save()

    import datetime
    CareerPosition.objects.filter(section=section).delete()
    positions = [
        ("Production Manager", "Full-time", "Ashulia, Dhaka", "Production", "Oversee daily production operations, manage production floor team, ensure quality output and on-time delivery targets."),
        ("Quality Control Inspector", "Full-time", "Ashulia, Dhaka", "Quality", "Inspect garments at various production stages, maintain QC reports, coordinate with production team on defect resolution."),
        ("Merchandiser", "Full-time", "Dhaka Office", "Merchandising", "Manage buyer communication, order follow-up, sample coordination, and shipment tracking for international accounts."),
        ("IE Engineer", "Full-time", "Ashulia, Dhaka", "Industrial Engineering", "Time and motion study, line balancing, efficiency improvement, and production planning."),
        ("HR Officer", "Full-time", "Ashulia, Dhaka", "Human Resources", "Recruitment, employee relations, payroll management, and compliance with labor laws."),
        ("Compliance Officer", "Full-time", "Ashulia, Dhaka", "Compliance", "Maintain compliance certifications, conduct internal audits, coordinate with buyers on compliance requirements."),
    ]
    for title, type_, location, dept, desc in positions:
        CareerPosition.objects.create(
            section=section,
            title=title,
            type=type_,
            location=location,
            department=dept,
            description=desc,
            posted_at=datetime.date.today(),
            status="active",
        )
    print(f"  ✅ Career: {len(positions)} positions created\n")


def seed_faq():
    print("❓ Seeding FAQ...")
    faq_section, _ = FAQSection.objects.get_or_create(id=1)
    faq_section.title = "Frequently Asked Questions"
    faq_section.subtitle = "Get answers to common questions about Humana Apparels"
    faq_section.save()

    FAQ.objects.filter(section=faq_section).delete()
    faqs = [
        ("What products does Humana Apparels manufacture?",
         "Humana Apparels specializes in high-quality woven garments including men's and ladies' shirts, trousers, jackets, dresses, and casual wear for international fashion brands."),
        ("What is the minimum order quantity (MOQ)?",
         "Our standard MOQ varies by product type. For basic items, MOQ starts from 1,000 pieces per style. Please contact our sales team for specific product MOQ details."),
        ("Which countries do you export to?",
         "We export to USA, Canada, UK, Germany, France, Italy, Spain, Poland, Japan, Korea, Brazil, Australia and many more countries across North America, Europe, and Asia-Pacific."),
        ("What compliance certifications do you hold?",
         "Humana Apparels holds BSCI, ISO 9001:2015, OEKO-TEX Standard 100, and is a LEED-certified green factory. We comply with all major international labor and environmental standards."),
        ("What is your average lead time?",
         "Standard lead time is 90-120 days from order confirmation to shipment. For repeat styles, we can often reduce this to 60-75 days."),
        ("Do you offer sampling services?",
         "Yes, we provide proto samples, fit samples, size sets, and pre-production samples. Sample lead time is typically 7-14 days depending on complexity."),
    ]
    for q, a in faqs:
        FAQ.objects.create(section=faq_section, question=q, answer=a)
    print(f"  ✅ FAQ: {len(faqs)} items\n")


def run_all():
    print("\n" + "="*50)
    print("🚀 HUMANA APPARELS — SEEDING ALL DATA")
    print("="*50 + "\n")

    seed_hero()
    seed_introduction()
    seed_stats()
    seed_services()
    seed_products()
    seed_gallery()
    seed_about()
    seed_activities()
    seed_contact()
    seed_career()
    seed_faq()

    print("="*50)
    print("✅ ALL DONE! Visit http://127.0.0.1:8000 to see the website")
    print("="*50 + "\n")


run_all()