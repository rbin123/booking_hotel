"""
Admin for bookings - view all, update status.
"""
from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'guest_name', 'check_in', 'check_out', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'check_in']
    search_fields = ['guest_name', 'guest_email', 'room__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
