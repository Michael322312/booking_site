from django.shortcuts import render, redirect, HttpResponse
from booking.models import Hotel, Room, Booking, User
from django_countries.data import COUNTRIES

# Create your views here.

def get_countries(request):
    countries = [ hotel.country for hotel in Hotel.objects.all() ]
    context = {
        "countries": countries
    }
    return render(
        request,
        "choose_country.html",
        context
    )

def get_hotels_in_country(request):
    hotels = Hotel.objects.filter(country=request.GET.get('country'))
    context = {
        "hotels": hotels,
        
    }
    return render(
        request,
        "country_hotels.html",
        context
    )

def get_hotel_rooms(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    context = {
        "hotel": hotel
    }
    return render(
        request,
        "hotel_rooms.html",
        context
    )

def booking_details(request, pk:int):
    booking = Booking.objects.get(id=pk)
    context = {
        "booking": booking
    }
    return render(
        request,
        "booking_details.html",
        context
    )


def booking_form(request, pk):
    if request.method == "GET":
        return render(request, "booking_form.html", {"room": Room.objects.get(id=pk)})
    elif request.method == "POST":
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        try:
            room = Room.objects.get(id=pk)
        except ValueError:
            return HttpResponse("Error! Value is not supported!", status=404)
        except Room.DoesNotExist:
            return HttpResponse("Error! Room number not found!", status=404)

        
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