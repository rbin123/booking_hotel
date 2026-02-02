"""
Forms for room search and display.
"""
from django import forms
from django.core.exceptions import ValidationError
from datetime import date


class RoomSearchForm(forms.Form):
    """Search form: check-in, check-out dates."""
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Check-in Date'
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Check-out Date'
    )

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        if check_in and check_out:
            if check_in < date.today():
                raise ValidationError({'check_in': 'Check-in date cannot be in the past.'})
            if check_out <= check_in:
                raise ValidationError({'check_out': 'Check-out must be after check-in.'})
        return cleaned
