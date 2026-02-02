"""
Room and Hotel models for the booking system.
"""
from django.db import models


class RoomCategory(models.Model):
    """Room type: Single, Double, Deluxe, Suite, Family."""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Room categories'

    def __str__(self):
        return self.name


class Hotel(models.Model):
    """Hotel property - can have multiple rooms."""
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    """Individual room belonging to a hotel and a category."""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)  # e.g. "Room 101"
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField(default=2)
    amenities = models.TextField(
        help_text='Comma-separated: WiFi, TV, AC, Mini Bar, etc.'
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['hotel', 'name']

    def __str__(self):
        return f"{self.hotel.name} - {self.name} ({self.category.name})"

    def get_amenities_list(self):
        """Return amenities as a list for display."""
        if not self.amenities:
            return []
        return [a.strip() for a in self.amenities.split(',') if a.strip()]


class RoomImage(models.Model):
    """Multiple images per room for gallery on detail page."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rooms/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary', 'id']

    def __str__(self):
        return f"Image for {self.room.name}"
