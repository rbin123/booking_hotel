"""
Management command to create default room categories.
Run: python manage.py create_categories
"""
from django.core.management.base import BaseCommand
from rooms.models import RoomCategory


CATEGORIES = [
    ('Single Room', 'single-room'),
    ('Double Room', 'double-room'),
    ('Deluxe Room', 'deluxe-room'),
    ('Suite Room', 'suite-room'),
    ('Family Room', 'family-room'),
]


class Command(BaseCommand):
    help = 'Create default room categories (Single, Double, Deluxe, Suite, Family)'

    def handle(self, *args, **options):
        created = 0
        for name, slug in CATEGORIES:
            _, was_created = RoomCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))
        if created == 0:
            self.stdout.write('All categories already exist.')
        else:
            self.stdout.write(self.style.SUCCESS(f'Created {created} category(ies).'))
