"""
Booking model for room reservations.
"""
from django.db import models
from django.conf import settings
from rooms.models import Room


class Booking(models.Model):
    """Room booking with check-in/out, guests, and status."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    guest_name = models.CharField(max_length=200, blank=True)
    guest_email = models.EmailField(blank=True)
    guest_phone = models.CharField(max_length=20, blank=True)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.room} - {self.check_in} to {self.check_out} ({self.status})"

    def get_nights(self):
        """Number of nights for this booking."""
        return (self.check_out - self.check_in).days

    def save(self, *args, **kwargs):
        if self.room and self.check_in and self.check_out:
            nights = (self.check_out - self.check_in).days
            self.total_price = self.room.price_per_night * nights
        super().save(*args, **kwargs)
