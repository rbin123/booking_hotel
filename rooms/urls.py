"""
URL configuration for rooms app.
"""
from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.home, name='home'),
    path('hotels/', views.HotelListView.as_view(), name='hotel_list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
]
