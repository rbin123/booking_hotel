"""
Management command to create 10 hotels and 10 rooms per category (50 rooms total).
Run: python manage.py create_sample_data
"""
from decimal import Decimal
from django.core.management.base import BaseCommand
from rooms.models import Hotel, RoomCategory, Room


# 10 sample hotels
HOTELS = [
    {"name": "Grand Plaza Hotel", "address": "100 Main Street, Downtown", "phone": "+1 555-100-1000", "email": "info@grandplaza.com"},
    {"name": "Sunset Resort & Spa", "address": "200 Ocean Drive, Beachfront", "phone": "+1 555-200-2000", "email": "hello@sunsetresort.com"},
    {"name": "Mountain View Lodge", "address": "300 Pine Road, Hillside", "phone": "+1 555-300-3000", "email": "stay@mountainview.com"},
    {"name": "City Center Inn", "address": "400 Commerce Ave, City Center", "phone": "+1 555-400-4000", "email": "book@citycenterinn.com"},
    {"name": "Riverside Suites", "address": "500 River Road, Riverside", "phone": "+1 555-500-5000", "email": "info@riversidesuites.com"},
    {"name": "Garden Hotel", "address": "600 Bloom Street, Garden District", "phone": "+1 555-600-6000", "email": "contact@gardenhotel.com"},
    {"name": "Lakeside Retreat", "address": "700 Lake View Drive", "phone": "+1 555-700-7000", "email": "reservations@lakesideretreat.com"},
    {"name": "Heritage Grand", "address": "800 Historic Square", "phone": "+1 555-800-8000", "email": "guest@heritagegrand.com"},
    {"name": "Skyline Tower Hotel", "address": "900 Skyline Blvd, Uptown", "phone": "+1 555-900-9000", "email": "book@skylinetower.com"},
    {"name": "Parkside Inn", "address": "1000 Park Avenue, Green Zone", "phone": "+1 555-000-0000", "email": "hello@parksideinn.com"},
]

# Price range and max guests per category (category_slug -> (min_price, max_price, max_guests))
CATEGORY_ROOM_CONFIG = {
    "single-room": (Decimal("59.00"), Decimal("89.00"), 1),
    "double-room": (Decimal("89.00"), Decimal("129.00"), 2),
    "deluxe-room": (Decimal("129.00"), Decimal("189.00"), 3),
    "suite-room": (Decimal("189.00"), Decimal("299.00"), 4),
    "family-room": (Decimal("149.00"), Decimal("249.00"), 6),
}

DEFAULT_AMENITIES = "WiFi, TV, AC, Mini Bar, Safe, Coffee Maker"
ROOM_DESCRIPTION = "Comfortable and well-appointed room with modern amenities. Perfect for your stay."


class Command(BaseCommand):
    help = "Create 10 hotels and 10 rooms per category (50 rooms total)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing hotels and rooms before creating (keeps categories).",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            Room.objects.all().delete()
            Hotel.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing rooms and hotels."))

        # Ensure categories exist
        categories = list(RoomCategory.objects.all().order_by("slug"))
        if len(categories) != 5:
            self.stdout.write(self.style.ERROR("Run 'python manage.py create_categories' first."))
            return

        # Create 10 hotels
        hotels = []
        for i, data in enumerate(HOTELS):
            hotel, created = Hotel.objects.get_or_create(
                name=data["name"],
                defaults={
                    "address": data["address"],
                    "phone": data.get("phone", ""),
                    "email": data.get("email", ""),
                    "description": f"Welcome to {data['name']}. We offer comfortable rooms and great service.",
                    "is_active": True,
                },
            )
            hotels.append(hotel)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created hotel: {hotel.name}"))

        if len(hotels) < 10:
            # Create additional hotels if we had some existing
            existing_names = {h.name for h in hotels}
            for data in HOTELS:
                if data["name"] not in existing_names:
                    hotel = Hotel.objects.create(
                        name=data["name"],
                        address=data["address"],
                        phone=data.get("phone", ""),
                        email=data.get("email", ""),
                        description=f"Welcome to {data['name']}. We offer comfortable rooms and great service.",
                        is_active=True,
                    )
                    hotels.append(hotel)
                    existing_names.add(hotel.name)
                    self.stdout.write(self.style.SUCCESS(f"Created hotel: {hotel.name}"))
                if len(hotels) >= 10:
                    break
        hotels = hotels[:10]

        # Create 10 rooms per category (50 rooms)
        room_count = 0
        for category in categories:
            config = CATEGORY_ROOM_CONFIG.get(category.slug)
            if not config:
                continue
            low, high, max_guests = config
            step = (high - low) / 9 if high != low else Decimal("0")
            amenities = DEFAULT_AMENITIES
            for i in range(10):
                hotel = hotels[i % len(hotels)]
                price = low + (step * i)
                room_name = f"{category.name} {100 + i}"
                _, created = Room.objects.get_or_create(
                    hotel=hotel,
                    name=room_name,
                    defaults={
                        "category": category,
                        "description": ROOM_DESCRIPTION,
                        "price_per_night": price,
                        "max_guests": max_guests,
                        "amenities": amenities,
                        "is_available": True,
                    },
                )
                if created:
                    room_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created 10 rooms for category: {category.name}"))

        self.stdout.write(self.style.SUCCESS(f"Done. {len(hotels)} hotels, {room_count} new rooms created (10 per category)."))
