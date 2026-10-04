from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import SimpleTestCase

from hapl.models import CompanyStats, GalleryPage, HomeCarouselSlide, HomeHeroSection


class HomepageRenderingTests(SimpleTestCase):
    """Check CMS-dependent states without modifying the local database."""

    def render_home(self, **context):
        return render_to_string("www/home.html", context)

    def test_empty_content_renders_without_fabricated_facts(self):
        html = self.render_home()
        self.assertIn("Quality Apparel,", html)  # hero fallback title
        self.assertNotIn("data-count-to", html)
        self.assertNotIn("+880000000000", html)
        self.assertNotIn("tel:", html)

    def test_hero_uses_admin_copy_and_cta(self):
        hero = HomeHeroSection(
            title="Configured hero title",
            subtitle="Configured supporting copy",
            cta_primary_active=True,
            cta_primary_text="Request a sample",
            cta_primary_url="/contact/?topic=sample",
            cta_secondary_active=False,
            cta_secondary_text="Hidden action",
        )
        html = self.render_home(hero=hero, slides=[])
        self.assertIn(">Configured</span>", html)
        self.assertIn("Configured supporting copy", html)
        self.assertIn('href="/contact/?topic=sample"', html)
        self.assertNotIn("Hidden action", html)

    def test_disabled_blank_ctas_do_not_gain_fallback_actions(self):
        section = SimpleNamespace(
            cta_primary_active=False, cta_secondary_active=False,
            cta_primary_text="", cta_secondary_text="",
        )
        html = render_to_string(
            "www/partials/home_hero.html", {"hero": {"section": section}}
        )
        self.assertNotIn("Explore our products", html)
        self.assertNotIn("Our company</a>", html)

    def test_stats_render_number_and_label(self):
        html = self.render_home(stats=[CompanyStats(number=150000, label="Pcs / Month")])
        self.assertIn('data-count-to="150000"', html)
        self.assertIn("150,000", html)
        self.assertIn("Pcs / Month", html)

    def test_legacy_stat_value_remains_available_as_fallback(self):
        html = self.render_home(stats=[CompanyStats(title="Metric", value="09+")])
        self.assertIn("09+", html)
        self.assertIn("Metric", html)

    def test_single_slide_does_not_render_unused_controls(self):
        slide = HomeCarouselSlide(image="home/carousel/a.webp", alt_text="Factory")
        html = self.render_home(slides=[slide])
        self.assertIn('aria-label="1 / 1"', html)
        self.assertNotIn("data-hero-prev", html)

    def test_navigation_respects_admin_visibility(self):
        html = render_to_string(
            "www/partials/home_header.html",
            {"navbar": SimpleNamespace(show_home=True, show_products=False)},
        )
        self.assertIn('aria-current="page"', html)
        self.assertNotIn('href="/products/"', html)

    def test_virtual_tour_is_cms_controlled(self):
        self.assertIn("360vr.hameemgroup.com/humana/", self.render_home())
        hidden = self.render_home(gallery_page=GalleryPage(tour_url=None))
        self.assertNotIn('id="virtual-tour"', hidden)
        custom = self.render_home(gallery_page=GalleryPage(tour_url="https://example.com/tour", tour_title="Custom tour"))
        self.assertIn('href="https://example.com/tour"', custom)
        self.assertIn("Custom tour", custom)
