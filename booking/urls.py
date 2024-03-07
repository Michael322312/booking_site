from django.urls import path 
from .views import *

urlpatterns = [
    path('', get_countries),
    path('country_hotels', get_hotels_in_country),
    path('hotel/<int:hotel_id>', get_hotel_rooms),
    path('booking/<int:pk>', booking_form),
    path('booking_details/<int:pk>', booking_details, name="booking_details")
] 