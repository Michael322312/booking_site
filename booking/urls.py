from django.urls import path 
from .views import *

urlpatterns = [
    path('', get_countries, name="countries"),
    path('country_hotels', get_hotels_in_country, name="country_hotels"),
    path('hotel/<int:hotel_id>', get_hotel_rooms, name="hotel_rooms"),
    path('booking/<int:pk>', booking_form, name="booking_form"),
    path('booking_details/<int:pk>', booking_details, name="booking_details"),
    path('user_info', get_user_info, name="user_info"),
    path('user_bookings', get_user_bookings, name="user_bookings")
] 