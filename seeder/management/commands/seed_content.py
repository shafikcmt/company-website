import logging
from django.core.management.base import BaseCommand
from seeder.content_seeder import (
    SiteSeeder,
    HomeSeeder,
    AboutSeeder,
    CustomerSeeder,
    ContactSeeder,
    CareerSeeder,
    ActivitiesSeeder,
    ProductsSeeder,
    ComplianceSeeder,
    SustainabilitySeeder,
    GallerySeeder,
)

logger = logging.getLogger(__name__)

# Map of all available seeders
SEEDERS = {
    "site": SiteSeeder,
    "home": HomeSeeder,
    "about": AboutSeeder,
    "customers": CustomerSeeder,
    "contact": ContactSeeder,
    "career": CareerSeeder,
    "activities": ActivitiesSeeder,
    "products": ProductsSeeder,
    "compliance": ComplianceSeeder,
    "sustainability": SustainabilitySeeder,
    "gallery": GallerySeeder,
}


class Command(BaseCommand):
    help = "Seeds the database with realistic demo content"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Delete existing data before seeding",
        )
        parser.add_argument(
            "pages",
            nargs="*",
            type=str,
            help="Specific pages to seed (e.g., home about products). Seeds all if none specified.",
        )

    def handle(self, *args, **options):
        clean = options["clean"]
        requested_pages = options["pages"]

        # If no specific pages requested, seed all
        if not requested_pages:
            pages_to_seed = list(SEEDERS.keys())
        else:
            # Validate the requested pages
            invalid_pages = [page for page in requested_pages if page not in SEEDERS]
            if invalid_pages:
                self.stderr.write(
                    self.style.ERROR(
                        f"Error: Invalid page(s): {', '.join(invalid_pages)}. "
                        f"Available pages: {', '.join(SEEDERS.keys())}"
                    )
                )
                return
            pages_to_seed = requested_pages

        logger.info(f"🚀 Starting data seeding for: {', '.join(pages_to_seed)}...")

        # Run the selected seeders
        for page in pages_to_seed:
            seeder_class = SEEDERS[page]
            seeder_class(clean=clean).run()

        logger.info("🎉 Data seeding complete!")
