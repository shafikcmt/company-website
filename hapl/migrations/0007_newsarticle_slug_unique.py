from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hapl", "0006_populate_newsarticle_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsarticle",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
