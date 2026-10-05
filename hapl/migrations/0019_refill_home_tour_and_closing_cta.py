from django.db import migrations


# 0018 filled these on rows that existed when it ran. Rows created after it
# (e.g. by an older `seed_content --clean`) were left empty, which hides the
# home page's 360° tour block. Fill the empty fields again; values editors
# have set are kept.
HERO_CLOSING = {
    "closing_eyebrow": "Let’s work together",
    "closing_title": "Your next collection. Our next conversation.",
    "closing_button_text": "Talk to our team",
    "closing_button_url": "/contact/",
}
GALLERY_HOME = {
    "home_eyebrow": "Inside Humana",
    "home_title": "A closer look at our facilities.",
    "tour_url": "https://360vr.hameemgroup.com/humana/",
    "tour_eyebrow": "Virtual experience",
    "tour_title": "Explore Humana Apparels in 360°",
    "tour_text": (
        "Take an immersive virtual tour of our manufacturing facility and "
        "explore Humana Apparels from a new perspective."
    ),
    "tour_button_text": "Explore 360° Factory Tour",
}


def refill(apps, schema_editor):
    for model_name, values in (("HomeHeroSection", HERO_CLOSING), ("GalleryPage", GALLERY_HOME)):
        model = apps.get_model("hapl", model_name)
        for obj in model.objects.filter(deleted__isnull=True):
            empty = {field: value for field, value in values.items() if getattr(obj, field) in (None, "")}
            if empty:
                model.objects.filter(pk=obj.pk).update(**empty)


class Migration(migrations.Migration):

    dependencies = [
        ("hapl", "0018_home_tour_and_closing_cta"),
    ]

    operations = [
        migrations.RunPython(refill, migrations.RunPython.noop),
    ]
