"""
Views for rooms: home, hotel list, room list, room detail, search.
"""
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Hotel, Room, RoomCategory
from .forms import RoomSearchForm
from bookings.models import Booking


def home(request):
    """Landing page with search form."""
    form = RoomSearchForm(request.GET or None)
    categories = RoomCategory.objects.all()
    hotels = Hotel.objects.filter(is_active=True)[:6]
    context = {
        'form': form,
        'categories': categories,
        'hotels': hotels,
    }
    return render(request, 'rooms/home.html', context)


class HotelListView(ListView):
    """List all active hotels."""
    model = Hotel
    template_name = 'rooms/hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 9

    def get_queryset(self):
        return Hotel.objects.filter(is_active=True).order_by('name')


class HotelDetailView(DetailView):
    """Hotel detail with its rooms."""
    model = Hotel
    template_name = 'rooms/hotel_detail.html'
    context_object_name = 'hotel'


def room_list(request):
    """
    List rooms with optional search by check-in/check-out and category.
    Shows only available rooms for the given dates if dates provided.
    """
    form = RoomSearchForm(request.GET or None)
    rooms = Room.objects.filter(is_available=True).select_related('hotel', 'category').order_by('hotel', 'category')

    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        rooms = rooms.filter(category__slug=category_slug)

    check_in = None
    check_out = None
    if form.is_valid():
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']
        # Exclude rooms that have overlapping bookings
        overlapping = Booking.objects.filter(
            status='confirmed',
        ).filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
        ).values_list('room_id', flat=True)
        rooms = rooms.exclude(id__in=overlapping)

    categories = RoomCategory.objects.all()
    context = {
        'rooms': rooms,
        'form': form,
        'categories': categories,
        'check_in': check_in,
        'check_out': check_out,
    }
    return render(request, 'rooms/room_list.html', context)


def room_detail(request, pk):
    """Room detail page with images, amenities, and booking form link."""
    room = get_object_or_404(Room.objects.select_related('hotel', 'category').prefetch_related('images'), pk=pk)
    # Primary image or first image
    primary_image = room.images.filter(is_primary=True).first() or room.images.first()
    context = {
        'room': room,
        'primary_image': primary_image,
    }
    return render(request, 'rooms/room_detail.html', context)
