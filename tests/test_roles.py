from django.test import TestCase
from django.urls import reverse

from users.models import Role, User
from users.roles import ROLE_NAMES, role_models, sync_roles


class RoleAccessTests(TestCase):
    """Section roles limit an editor to their part of the website."""

    @classmethod
    def setUpTestData(cls):
        sync_roles()
        cls.editor = User.objects.create_user("gallery-editor", password="pw-12345-x", is_staff=True)
        cls.editor.roles.add(Role.objects.get(name="Gallery"))

    def setUp(self):
        self.client.force_login(self.editor)

    def test_default_roles_exist_with_all_four_permissions_per_model(self):
        for name in ROLE_NAMES:
            with self.subTest(role=name):
                role = Role.objects.get(name=name)
                self.assertEqual(role.permissions.count(), len(role_models(name)) * 4)

    def test_editor_can_open_their_section(self):
        for url_name in ("admin:index", "admin:hapl_gallerypage_changelist", "admin:hapl_galleryimage_add"):
            with self.subTest(url=url_name):
                self.assertEqual(self.client.get(reverse(url_name), follow=True).status_code, 200)

    def test_editor_cannot_open_other_sections_or_users(self):
        for url_name in ("admin:hapl_product_changelist", "admin:hapl_sitesettings_changelist", "admin:users_user_changelist"):
            with self.subTest(url=url_name):
                self.assertEqual(self.client.get(reverse(url_name), follow=True).status_code, 403)

    def test_sidebar_and_dashboard_only_show_allowed_sections(self):
        html = self.client.get(reverse("admin:index")).content.decode()
        self.assertIn(reverse("admin:hapl_galleryimage_changelist"), html)
        self.assertNotIn(reverse("admin:hapl_product_changelist"), html)
        self.assertNotIn(reverse("admin:users_user_changelist"), html)
        self.assertNotIn("Open positions", html)

    def test_inactive_user_loses_role_permissions(self):
        self.editor.is_active = False
        self.editor.save()
        user = User.objects.get(pk=self.editor.pk)
        self.assertFalse(user.has_perm("hapl.view_gallerypage"))

    def test_sync_roles_keeps_edits_unless_reset(self):
        role = Role.objects.get(name="Gallery")
        role.permissions.clear()
        sync_roles()
        self.assertEqual(role.permissions.count(), 0)
        sync_roles(reset=True)
        self.assertEqual(role.permissions.count(), 16)


class UserAdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("boss", "boss@example.com", "pw-12345-x")
        self.client.force_login(self.admin)
        sync_roles()

    def test_superuser_creates_an_editor_with_a_role(self):
        gallery = Role.objects.get(name="Gallery")
        response = self.client.post(
            reverse("admin:users_user_add"),
            {
                "username": "newbie",
                "email": "newbie@example.com",
                "first_name": "New",
                "last_name": "Editor",
                "password1": "Strong-pass-9876",
                "password2": "Strong-pass-9876",
                "roles": [gallery.pk],
            },
        )
        self.assertEqual(response.status_code, 302, response.content[:2000])
        user = User.objects.get(username="newbie")
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(list(user.roles.all()), [gallery])
        self.assertTrue(user.has_perm("hapl.change_galleryimage"))
        self.assertFalse(user.has_perm("hapl.change_product"))

    def test_user_and_role_lists_render(self):
        for url_name in ("admin:users_user_changelist", "admin:users_role_changelist", "admin:users_user_add"):
            with self.subTest(url=url_name):
                self.assertEqual(self.client.get(reverse(url_name)).status_code, 200)
