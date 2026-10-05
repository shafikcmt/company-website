from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from django.db.models import Q
from users.models import User


# --- AUTHENTICATION BACKENDS ---


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        try:
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def _get_group_permissions(self, user_obj):
        # Permissions from groups, the user's roles and their department, so
        # has_perm / has_module_perms (and the admin) honour roles. Inactive
        # users get nothing: ModelBackend checks is_active before calling this.
        return Permission.objects.filter(
            Q(group__user=user_obj)
            | Q(roles__user=user_obj)
            | Q(departments__users=user_obj)
        ).distinct()

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
