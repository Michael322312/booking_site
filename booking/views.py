from django.shortcuts import render, redirect, HttpResponse
from booking.models import Hotel, Room, Booking
from django_countries.data import COUNTRIES
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

def get_countries(request):
    countries = [ hotel.country for hotel in Hotel.objects.all() ]
    context = {
        "countries": countries
    }
    return render(
        request,
        "booking/choose_country.html",
        context
    )

def get_hotels_in_country(request):
    hotels = Hotel.objects.filter(country=request.GET.get('country'))
    context = {
        "hotels": hotels,
    }
    return render(
        request,
        "booking/country_hotels.html",
        context
    )

@login_required
def get_user_info(request):
    user = request.user
    context = {
        "user": user
    }

    return render(
        request,
        "booking/account_page.html",
        context
    )



@login_required
def get_user_bookings(request):
    user = request.user
    user_bookings = Booking.objects.filter(user=user).all()

    context = {
        "user": user,
        "user_bookings": user_bookings
    }

    return render(
        request,
        "booking/user_bookings.html",
        context
    )


def get_hotel_rooms(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    context = {
        "hotel": hotel
    }
    return render(
        request,
        "booking/hotel_rooms.html",
        context
    )


def booking_details(request, pk:int):
    booking = Booking.objects.get(id=pk)
    context = {
        "booking": booking
    }
    return render(
        request,
        "booking/booking_details.html",
        context
    )


def booking_form(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "booking/booking_form.html", {"room": Room.objects.get(id=pk)})
        else:
            messages.error(request, "Unauthenicated users can't book rooms!")
            return redirect("hotel_rooms", hotel_id=Room.objects.get(id=pk).hotel.id)
    elif request.method == "POST":
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if start_time > end_time:
            messages.error(request, "Start time can't be more than end time")
            return redirect("booking_form", pk=pk)

        try:
            room = Room.objects.get(id=pk)
        except ValueError:
            return HttpResponse("Error! Value is not supported!", status=404)
        except Room.DoesNotExist:
            return HttpResponse("Error! Room number not found!", status=404)

        overlapping_bookings = Booking.objects.filter(Q(start_time__lt=end_time) & Q(end_time__gt=start_time) & Q(room=room))
        
        if overlapping_bookings.exists():
            messages.error(request, "This room is already has booking during this time")
            return redirect("booking_form", pk=pk)
        
        booking = Booking(
            room=room,
            start_time=start_time,
            end_time=end_time,
            user=request.user,
        )
        booking.save()
        return redirect('booking_details', pk=booking.id)
    else:
        return HttpResponse("Happened unexpected error!", status=404) 