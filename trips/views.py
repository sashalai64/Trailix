from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import requests
from django.conf import settings

from .models import *
from .forms import *


today = timezone.now().date()

def index(request):
    return render(request, "trips/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "trips/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "trips/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "trips/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "trips/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "trips/register.html")


@login_required
def trips(request):
    trip_type = request.GET.get('type')
    today = timezone.now().date()
    previous_trips = Trip.objects.filter(user = request.user, end_date__lt = today).order_by('-start_date')
    upcoming_trips = Trip.objects.filter(user = request.user, end_date__gte = today).order_by('-start_date')

    if trip_type == 'upcoming':
        return render(request, "trips/upcoming_trips.html", {
            "upcoming_trips": upcoming_trips,
        })
    elif trip_type == 'previous':
        return render(request, "trips/previous_trips.html", {
            "previous_trips": previous_trips
        })
    else:
        return render(request, "trips/all_trips.html", {
            "upcoming_trips": upcoming_trips,
            "previous_trips": previous_trips
        })
    

@login_required
def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)

        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save() 

            end_time = trip.end_date  
            if end_time > today:
                url = reverse('trips') + '?type=upcoming'
            else:
                url = reverse('trips') + '?type=previous'
            
            return redirect(url)
        
        else:
            return render(request, "trips/add_trip.html", {
                "form": form
            })

    return render(request, 'trips/add_trip.html', {
        "form": TripForm(),
    })


def get_cities(request):
    country_code = request.GET.get('country_code')
    query = request.GET.get('query')

    if not country_code or not query:
        return JsonResponse({'error': 'Country code and query are required'}, status=400)

    api_key = settings.RAPID_GEODB_API_KEY
    url = f'https://wft-geo-db.p.rapidapi.com/v1/geo/countries/{country_code}/places'
    querystring = {"namePrefix": query}
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': 'wft-geo-db.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers, params=querystring)
    return JsonResponse(response.json())