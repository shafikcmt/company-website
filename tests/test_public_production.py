import re
from html.parser import HTMLParser
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management import call_command
from django.template.loader import render_to_string
from django.test import SimpleTestCase, override_settings

from tests.storage_helpers import disposable_storage


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        self.urls.extend(value for key, value in attrs if key in ('src', 'href') and value)


class PublicProductionTests(SimpleTestCase):
    def test_shared_shell_uses_built_css_and_omits_unverified_contacts(self):
        for template in ('www/about.html', 'www/products.html', 'www/contact.html'):
            with self.subTest(template=template):
                html = render_to_string(template, {})
                self.assertIn('/static/css/public.styles.css', html)
                self.assertNotIn('cdn.tailwindcss.com', html)
                self.assertNotIn('tailwind.config', html)
                self.assertNotIn('tel:', html)
                self.assertNotIn('mailto:info@humanaapparels.com', html)
                self.assertNotIn('Dhaka, Bangladesh', html)
                self.assertIn('href="/contact/"', html)
                self.assertIn('public-site', html)

    def test_build_contains_shared_responsive_and_brand_utilities(self):
        css = (settings.BASE_DIR / 'common/static/css/public.styles.css').read_text()
        for selector in ('.bg-navy', '.text-amber', '.container-site', '.font-sans', '.hidden',
                         '.lg\\:grid-cols-4', '.md\\:flex', '.size-9', '.prose'):
            with self.subTest(selector=selector):
                self.assertIn(selector, css)
        self.assertNotIn('@tailwind ', css)

    def test_production_collection_and_manifest_resolve_public_assets(self):
        # Exercise the production pipeline in disposable storage, not STATIC_ROOT.
        with disposable_storage('hapl-static-') as root:
            with override_settings(DEBUG=False, STATIC_ROOT=root, STORAGES={
                'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
                'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'},
            }):
                call_command('collectstatic', interactive=False, verbosity=0)
                self.assertTrue((Path(root) / 'staticfiles.json').is_file())
                for template in ('www/about.html', 'www/products.html', 'www/contact.html'):
                    parser = AssetParser()
                    parser.feed(render_to_string(template, {}))
                    for url in parser.urls:
                        if url.startswith(settings.STATIC_URL):
                            name = url.removeprefix(settings.STATIC_URL)
                            self.assertTrue(staticfiles_storage.exists(name), (template, name))
                            self.assertRegex(name, r'\.[0-9a-f]{12}\.')
                # Check transitive CSS URLs, including the locally bundled icon font.
                for original in ('css/public.styles.css', 'css/about.css', 'css/phosphor-duotone.css'):
                    name = staticfiles_storage.stored_name(original)
                    with staticfiles_storage.open(name) as source:
                        css = source.read().decode()
                    for url in re.findall(r'url\([\'"]?([^\)\'\"]+)', css):
                        if url.startswith(('data:', 'http:', 'https:', '#')):
                            continue
                        target = url.removeprefix(settings.STATIC_URL) if url.startswith(settings.STATIC_URL) else str(Path(name).parent / url)
                        self.assertTrue(staticfiles_storage.exists(target), (name, target))
                # Assert release assets explicitly, even when empty CMS content
                # leaves conditional template references absent.
                for original in ('js/about.js', 'images/favicon/humana-centered-16.png',
                                 'images/favicon/humana-centered-32.png',
                                 'images/favicon/humana-centered-48.png'):
                    self.assertTrue(staticfiles_storage.exists(staticfiles_storage.stored_name(original)), original)
