from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm

from users.forms import (
    DepartmentAdminForm,
    RoleAdminForm,
    UserChangeForm,
    UserCreationForm,
)
from users.models import Department, Role, User


# --- UNREGISTER DEFAULT ADMIN CLASSES ---


admin.site.unregister(Group)


# --- REGISTER ADMIN CLASSES ---


ROLE_HELP = (
    "What this person can edit. Pick one or more website sections (e.g. "
    "Gallery, Career & HR). Roles are managed under System → Roles."
)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("username", "display_name", "email", "display_roles", "display_access", "last_login")
    list_filter = ("is_active", "is_superuser", "roles")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = ("roles", "user_permissions")

    fieldsets = (
        ("Account", {"fields": ("username", "password", "is_active")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Access",
            {
                "fields": ("roles", "is_superuser"),
                "description": (
                    "Roles decide which sections of the website this person can edit. "
                    "A superuser can edit everything, including users."
                ),
            },
        ),
        (
            "Advanced permissions",
            {"fields": ("department", "user_permissions", "is_staff"), "classes": ("collapse",)},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined"), "classes": ("collapse",)}),
    )
    add_fieldsets = (
        ("Account", {"fields": ("username", "email", "first_name", "last_name")}),
        ("Password", {"fields": ("password1", "password2")}),
        ("Access", {"fields": ("roles",)}),
    )
    readonly_fields = ("last_login", "date_joined")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "roles" in form.base_fields:
            form.base_fields["roles"].help_text = ROLE_HELP
        return form

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        # Only a superuser may grant superuser or raw permissions.
        if not request.user.is_superuser:
            fields += ["is_superuser", "is_staff", "user_permissions", "department"]
        return fields

    def get_queryset(self, request):
        # django-guardian's internal anonymous user is not a real account.
        anonymous = getattr(settings, "ANONYMOUS_USER_NAME", "AnonymousUser")
        return super().get_queryset(request).exclude(username=anonymous).prefetch_related("roles")

    @display(description="Name")
    def display_name(self, obj):
        return obj.get_full_name() or "—"

    @display(description="Roles")
    def display_roles(self, obj):
        if obj.is_superuser:
            return "All sections"
        names = [role.name for role in obj.roles.all()]
        return ", ".join(names) if names else "—"

    @display(
        description="Access",
        label={"Superuser": "success", "Editor": "info", "No access": "warning", "Inactive": "danger"},
    )
    def display_access(self, obj):
        if not obj.is_active:
            return "Inactive"
        if obj.is_superuser:
            return "Superuser"
        if obj.is_staff and obj.roles.exists():
            return "Editor"
        return "No access"


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    form = RoleAdminForm
    filter_horizontal = ("permissions",)
    list_display = ("name", "display_users", "display_permissions")
    search_fields = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            user_total=Count("user", distinct=True), permission_total=Count("permissions", distinct=True)
        )

    @display(description="Users", ordering="user_total")
    def display_users(self, obj):
        return obj.user_total

    @display(description="Permissions", ordering="permission_total")
    def display_permissions(self, obj):
        return obj.permission_total


@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    form = DepartmentAdminForm
    filter_horizontal = ("permissions",)
    list_display = ("name",)
