from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import SimpleTestCase


class HomepageRenderingTests(SimpleTestCase):
    """Check CMS-dependent states without modifying the local database."""

    def render_home(self, **context):
        return render_to_string("www/home.html", context)

    def test_empty_content_renders_without_fabricated_facts(self):
        html = self.render_home()
        self.assertIn("<h1>Humana Apparels</h1>", html)
        self.assertNotIn("home-fact", html)
        self.assertNotIn("+880000000000", html)
        self.assertNotIn('id="certificates-heading"', html)

    def test_hero_uses_admin_copy_and_cta(self):
        section = SimpleNamespace(
            title="Configured hero title",
            subtitle="Configured supporting copy",
            cta_primary_active=True,
            cta_primary_text="Request a sample",
            cta_primary_url="/contact/?topic=sample",
            cta_secondary_active=False,
            cta_secondary_text="Hidden action",
        )
        html = self.render_home(hero={"section": section, "slides": []})
        self.assertIn("<h1>Configured hero title</h1>", html)
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

    def test_company_facts_take_precedence_and_preserve_format(self):
        html = self.render_home(
            company_facts=[{"label": "Capacity", "value": "150,000", "subtext": "Pcs / Month"}],
            stats={"items": [{"title": "Legacy metric", "value": "09+"}]},
        )
        self.assertIn("<strong>150,000</strong>", html)
        self.assertIn("Pcs / Month", html)
        self.assertNotIn("Legacy metric", html)

    def test_legacy_stats_remain_available_as_fallback(self):
        html = self.render_home(stats={"items": [{"title": "Metric", "value": "09+"}]})
        self.assertIn("<strong>09+</strong>", html)

    def test_single_slide_does_not_render_unused_controls(self):
        html = self.render_home(hero={"slides": [{"title": "Factory"}]})
        self.assertIn('aria-label="1 of 1"', html)
        self.assertNotIn("data-home-controls", html)

    def test_navigation_respects_admin_visibility(self):
        html = render_to_string(
            "www/partials/home_header.html",
            {"navbar": SimpleNamespace(show_home=True, show_products=False)},
        )
        self.assertIn('aria-current="page"', html)
        self.assertNotIn('href="/products/"', html)

    def test_certificate_without_external_url_links_to_compliance(self):
        html = self.render_home(certificates=[{"name": "Configured certificate"}])
        self.assertIn('class="home-certificate" href="/compliance/"', html)
        self.assertIn("Configured certificate", html)
