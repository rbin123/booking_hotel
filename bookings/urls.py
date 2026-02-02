"""
URL configuration for bookings app.
"""
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:room_id>/', views.booking_create, name='create'),
    path('confirmation/<int:pk>/', views.booking_confirmation, name='confirmation'),
    path('history/', views.BookingHistoryView.as_view(), name='history'),
    path('cancel/<int:pk>/', views.booking_cancel, name='cancel'),
]
