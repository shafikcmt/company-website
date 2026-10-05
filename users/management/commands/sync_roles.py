from django.core.management.base import BaseCommand

from users.roles import sync_roles


class Command(BaseCommand):
    help = "Create the default content roles; --reset restores their default permissions."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Reset existing roles to the defaults.")

    def handle(self, *args, reset=False, **options):
        roles = sync_roles(reset=reset)
        self.stdout.write(self.style.SUCCESS(f"{len(roles)} role(s) created or reset."))
