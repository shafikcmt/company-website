from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _create_default_roles(sender, **kwargs):
    # Runs after hapl's permissions exist (auth creates them on post_migrate
    # for each app before this handler, which is connected later).
    from users.roles import sync_roles

    sync_roles()


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from django.apps import apps

        post_migrate.connect(
            _create_default_roles,
            sender=apps.get_app_config("hapl"),
            dispatch_uid="users.create_default_roles",
        )
