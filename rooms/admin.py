"""
Admin configuration for rooms app.
"""
from django.contrib import admin
from .models import RoomCategory, Hotel, Room, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'address']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel', 'category', 'price_per_night', 'max_guests', 'is_available']
    list_filter = ['category', 'hotel', 'is_available']
    search_fields = ['name', 'description']
    inlines = [RoomImageInline]
