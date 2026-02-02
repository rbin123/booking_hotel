"""
Booking views: create booking, confirmation, history, cancel.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import date
from .models import Booking
from .forms import BookingForm
from rooms.models import Room


def booking_create(request, room_id):
    """Create a new booking for a room."""
    room = get_object_or_404(Room.objects.select_related('hotel', 'category'), pk=room_id)
    form = BookingForm(request.POST or None, room=room)

    # Pre-fill from GET (search dates) or user
    if request.method == 'GET':
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
        if check_in:
            form.initial['check_in'] = check_in
        if check_out:
            form.initial['check_out'] = check_out
        if request.user.is_authenticated:
            form.initial['guest_name'] = request.user.get_full_name() or request.user.username
            form.initial['guest_email'] = request.user.email

    if form.is_valid():
        booking = form.save(commit=False)
        booking.room = room
        booking.user = request.user if request.user.is_authenticated else None
        booking.save()
        messages.success(request, 'Booking submitted successfully!')
        return redirect('bookings:confirmation', pk=booking.pk)

    context = {'form': form, 'room': room}
    return render(request, 'bookings/booking_form.html', context)


def booking_confirmation(request, pk):
    """Booking confirmation page with summary."""
    booking = get_object_or_404(
        Booking.objects.select_related('room', 'room__hotel', 'room__category'),
        pk=pk
    )
    context = {'booking': booking}
    return render(request, 'bookings/booking_confirmation.html', context)


class BookingHistoryView(LoginRequiredMixin, ListView):
    """User's booking history."""
    model = Booking
    template_name = 'bookings/booking_history.html'
    context_object_name = 'bookings'
    paginate_by = 10
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            'room', 'room__hotel', 'room__category'
        ).order_by('-created_at')


def booking_cancel(request, pk):
    """Cancel a booking (user or admin)."""
    booking = get_object_or_404(Booking, pk=pk)
    # Only allow cancel if user owns it or is staff
    if not (request.user == booking.user or request.user.is_staff):
        messages.error(request, 'You do not have permission to cancel this booking.')
        return redirect('bookings:history')
    if booking.status == 'cancelled':
        messages.info(request, 'This booking is already cancelled.')
        return redirect('bookings:history')
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking has been cancelled.')
    if request.user.is_staff and request.GET.get('next') == 'admin':
        return redirect('admin:bookings_booking_changelist')
    return redirect('bookings:history')
