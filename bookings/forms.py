"""
Booking form with dates, guests, and automatic price calculation.
"""
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from .models import Booking
from rooms.models import Room


class BookingForm(forms.ModelForm):
    """Booking form: check-in, check-out, num_guests, contact info."""
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_check_in'}),
        label='Check-in Date'
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_check_out'}),
        label='Check-out Date'
    )
    num_guests = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_num_guests'}),
        label='Number of Guests'
    )
    guest_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    guest_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    guest_phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = Booking
        fields = [
            'check_in', 'check_out', 'num_guests',
            'guest_name', 'guest_email', 'guest_phone', 'special_requests'
        ]

    def __init__(self, *args, room=None, **kwargs):
        self.room = room
        super().__init__(*args, **kwargs)
        if room:
            self.fields['num_guests'].validators.append(MaxValueValidator(room.max_guests))
            self.fields['num_guests'].help_text = f'Max {room.max_guests} guests for this room.'

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        num_guests = cleaned.get('num_guests')
        if check_in and check_out:
            if check_in < date.today():
                raise ValidationError({'check_in': 'Check-in date cannot be in the past.'})
            if check_out <= check_in:
                raise ValidationError({'check_out': 'Check-out must be after check-in.'})
        if self.room and num_guests and num_guests > self.room.max_guests:
            raise ValidationError({
                'num_guests': f'Maximum {self.room.max_guests} guests allowed for this room.'
            })
        return cleaned
