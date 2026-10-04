import importlib

import pytest
from django.urls import reverse

from hapl.models import (
    HomeHeroSection,
    HomeCarouselSlide,
    CompanyStats,
    SiteSettings,
    WhyUsSection,
    WhyUsFeature,
)
from users.models import User

PAGES = [
    "home",
    "about",
    "products",
    "customers",
    "complience",
    "sustainability",
    "gallery",
    "activities",
    "career",
    "contact",
]

populate = importlib.import_module("hapl.migrations.0017_populate_cms_defaults")


@pytest.fixture
def empty_db():
    """Remove the rows the data migration creates so pages render from fallbacks."""
    HomeHeroSection.objects.all().delete()
    SiteSettings.objects.all().delete()
    WhyUsFeature.objects.all().delete()
    WhyUsSection.objects.all().delete()


@pytest.mark.parametrize("name", PAGES)
def test_pages_render_on_empty_database(client, empty_db, name):
    response = client.get(reverse(name))
    assert response.status_code == 200


def test_home_uses_active_hero_and_its_active_slides(client):
    HomeHeroSection.objects.all().delete()
    HomeHeroSection.objects.create(title="Inactive hero", is_active=False)
    hero = HomeHeroSection.objects.create(
        title="Quality Apparel, Crafted Responsibly", highlight_word="crafted"
    )
    other = HomeHeroSection.objects.create(title="Second hero")
    HomeCarouselSlide.objects.create(section=hero, image="a.jpg", order=2, alt_text="Second")
    HomeCarouselSlide.objects.create(section=hero, image="b.jpg", order=1, alt_text="First")
    HomeCarouselSlide.objects.create(section=hero, image="c.jpg", is_active=False)
    HomeCarouselSlide.objects.create(section=other, image="d.jpg", alt_text="Other hero")

    response = client.get(reverse("home"))

    assert response.context["hero"] == hero
    assert [s.alt_text for s in response.context["slides"]] == ["First", "Second"]
    assert b'class="hero-word hero-reveal text-amber"' in response.content


def test_title_words_flag_highlight():
    hero = HomeHeroSection(title="Quality Apparel, Crafted Responsibly", highlight_word="crafted responsibly")
    words = hero.title_words()
    assert [w["text"] for w in words if w["highlight"]] == ["Crafted", "Responsibly"]
    assert [w["text"] for w in words if not w["highlight"]] == ["Quality", "Apparel,"]


def test_company_stats_keeps_legacy_value_in_sync():
    stat = CompanyStats.objects.create(number=2400, suffix="+", label="Skilled workers")
    assert stat.value == "2,400+"
    assert stat.title == "Skilled workers"
    assert stat.display_label == "Skilled workers"


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("38+", ("", 38, "+")),
        ("2,400+", ("", 2400, "+")),
        ("98%", ("", 98, "%")),
        ("$5M", ("$", 5, "M")),
        ("1.5M", None),
        ("American", None),
    ],
)
def test_stat_value_parser(raw, expected):
    assert populate.parse_stat_value(raw) == expected


def test_singleton_admin_redirects_to_the_single_row(client):
    admin = User.objects.create_superuser("root", "root@example.com", "pw")
    client.force_login(admin)
    site = SiteSettings.load()
    response = client.get(reverse("admin:hapl_sitesettings_changelist"))
    assert response.status_code == 302
    assert response.url == reverse("admin:hapl_sitesettings_change", args=[site.pk])
    assert client.get(reverse("admin:hapl_sitesettings_add")).status_code == 403
