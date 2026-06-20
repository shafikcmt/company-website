from django.db import migrations
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    """Back-fill a unique slug for every existing NewsArticle row.

    The model's own save() isn't available on the historical model used in
    migrations, so the slug generation logic is replicated here.
    """
    NewsArticle = apps.get_model("hapl", "NewsArticle")
    used_slugs = set()

    for article in NewsArticle.objects.all().order_by("pk"):
        base_slug = slugify(article.title) or f"news-{article.pk}"
        slug = base_slug
        counter = 1
        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        used_slugs.add(slug)
        article.slug = slug
        article.save(update_fields=["slug"])


def reverse_slugs(apps, schema_editor):
    """Reverse: clear slugs so the field can go back to blank."""
    NewsArticle = apps.get_model("hapl", "NewsArticle")
    NewsArticle.objects.update(slug="")


class Migration(migrations.Migration):

    dependencies = [
        ("hapl", "0005_garments_site_updates"),
    ]

    operations = [
        migrations.RunPython(populate_slugs, reverse_slugs),
    ]
