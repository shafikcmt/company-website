import io
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase
from PIL import Image

from common.services.image import ImageOptimizer
from common.templatetags.public_content import public_social_url
from hapl.admin import FAQInline, TeamMemberInline
from hapl.models import AboutSection, CompanyStats, FAQ, FAQSection, TeamMember, TeamSection
from hapl.views import about


class AboutCMSHardeningTests(SimpleTestCase):
    def test_optional_social_urls_are_validated_and_preserved(self):
        for value in [None, '', '#', 'javascript:alert(1)', 'ftp://example.com', 'not-a-url']:
            self.assertEqual(public_social_url(value), '')
        url = 'https://www.youtube.com/@approved?view=1&sort=2'
        self.assertEqual(public_social_url(url), url)
        html = render_to_string('www/about.html', {'site': SimpleNamespace(site_name='Approved Name', youtube_url=url, facebook_url='#')})
        self.assertIn('https://www.youtube.com/@approved?view=1&amp;sort=2', html)
        self.assertNotIn('aria-label="Facebook"', html)
        self.assertIn('About Us — Approved Name', html)

    def test_empty_content_has_no_social_placeholders_or_media_urls(self):
        html = render_to_string('www/about.html', {})
        for label in ['Facebook', 'LinkedIn', 'YouTube', 'Instagram']:
            self.assertNotIn(f'aria-label="{label}"', html)
        self.assertNotIn('src="/media/', html)
        self.assertIn('About Us', html)

    def test_about_queries_have_deterministic_order_without_evaluation(self):
        with patch('hapl.views.AboutSection.objects.first', return_value=None), patch('hapl.views.TeamSection.objects.first', return_value=None), patch('hapl.views.FAQSection.objects.first', return_value=None), patch('hapl.views.render', side_effect=lambda request, template, context: context):
            context = about(RequestFactory().get('/about/'))
        self.assertEqual(context['key_facts'].query.order_by, ('pk',))
        self.assertEqual(context['key_facts'].query.high_mark, 4)
        for queryset in [context['team']['management'], context['team']['staff'], context['faq']['faqs']]:
            self.assertEqual(queryset.query.order_by, ('order', 'pk'))

    def test_guidance_is_shared_by_standalone_and_inline_forms(self):
        request = RequestFactory().get('/admin/')
        editors = [admin.site._registry[TeamMember], TeamMemberInline(TeamSection, admin.site)]
        for editor in editors:
            field = editor.formfield_for_dbfield(TeamMember._meta.get_field('is_management'), request)
            self.assertEqual(field.label, 'Display in management group')
            self.assertIn('NOT a visibility control', field.help_text)
            self.assertEqual(editor.ordering, ('order', 'pk'))
        for editor in [admin.site._registry[FAQ], FAQInline(FAQSection, admin.site)]:
            field = editor.formfield_for_dbfield(FAQ._meta.get_field('order'), request)
            self.assertIn('equal values use record ID', field.help_text)
        self.assertEqual(admin.site._registry[CompanyStats].ordering, ('pk',))
        self.assertEqual(TeamMember._meta.get_field('is_management').verbose_name, 'is management')

    def test_about_upload_bounds_compression_and_no_upscaling(self):
        field = AboutSection._meta.get_field('image')
        self.assertEqual(field.max_dimensions, (1920, 1440))
        self.assertEqual(TeamMember._meta.get_field('image').max_dimensions, (400, 400))
        for dimensions, expected in [((3000, 2000), (1920, 1280)), ((2000, 3000), (960, 1440)), ((800, 600), (800, 600))]:
            source = io.BytesIO()
            Image.new('RGB', dimensions, '#476677').save(source, 'PNG')
            upload = SimpleUploadedFile('source.png', source.getvalue(), content_type='image/png')
            optimized = ImageOptimizer.optimize_image(upload, max_dimensions=field.max_dimensions)
            with Image.open(optimized) as image:
                self.assertEqual(image.size, expected)
                self.assertEqual(image.format, 'WEBP')
