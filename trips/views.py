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
from django.core.cache import cache
import time
from datetime import datetime
import pytz

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


def get_weather(trips):
    api_key = settings.RAPID_WEATHER_API_KEY
    url = "https://yahoo-weather5.p.rapidapi.com/weather"

    weather_data = {}
    fetched_cities = {}  # Track already fetched cities' weather data
    
    for trip in trips:
        if trip.city not in fetched_cities:
            cache_key = f"weather_{trip.city}"
            weather = cache.get(cache_key)

            if not weather:
                querystring = {"location": trip.city, "format": "json", "u": "c"}
                headers = {
                    "x-rapidapi-key": api_key,
                    "x-rapidapi-host": "yahoo-weather5.p.rapidapi.com"
                }

                try:
                    response = requests.get(url, headers=headers, params=querystring)
                    response.raise_for_status()
                    weather = response.json()
                    cache.set(cache_key, weather, timeout=1800) # Cache for 30 minutes

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching weather data for {trip.city}: {e}")
                    weather = {}

            fetched_cities[trip.city] = weather  # Store the fetched weather data for reuse
        else:
            weather = fetched_cities[trip.city]

        # Parse weather data
        try:
            if 'current_observation' in weather:
                condition_code = weather['current_observation']['condition'].get('code', None)
                temperature = weather['current_observation']['condition'].get('temperature', None)
                condition_text = weather['current_observation']['condition'].get('text', "N/A")
            else:
                condition_code = None
                temperature = None
                condition_text = "N/A"

        except (KeyError, ValueError) as e:
            condition_code = None
            temperature = None
            condition_text = "N/A"

        # Store parsed weather data in the dictionary
        weather_data[trip.id] = {
            'condition_code': condition_code,
            'temperature': temperature,
            'condition_text': condition_text
        }

    return weather_data


@login_required
def trips(request):
    trip_type = request.GET.get('type')
    today = timezone.now().date()
    upcoming_trips = Trip.objects.filter(user = request.user, end_date__gte = today).order_by('-start_date')
    previous_trips = Trip.objects.filter(user = request.user, end_date__lt = today).order_by('-start_date')
    
    upcoming_weather_data = get_weather(upcoming_trips)
    previous_weather_data = get_weather(previous_trips)

    for trip in upcoming_trips:
        trip.timezone = get_timezone(trip.lat, trip.lng)
    for trip in previous_trips:
        trip.timezone = get_timezone(trip.lat, trip.lng)

    if trip_type == 'upcoming':
        return render(request, "trips/upcoming_trips.html", {
            "upcoming_trips": upcoming_trips,
            "weather_data": upcoming_weather_data
        })
    elif trip_type == 'previous':
        return render(request, "trips/previous_trips.html", {
            "previous_trips": previous_trips,
            "weather_data": previous_weather_data
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
                "message": "Please select a city from the dropdown menu.",
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


def convert_to_timezone(timeZoneId):
    #Get the current UTC time
    utc_time = datetime.now(pytz.utc)
    
    #Convert UTC time to the target timezone
    target_time =  pytz.timezone(timeZoneId)
    local_time = utc_time.astimezone(target_time)

    #Return the formatted local date and time ('YYYY-MM-DD HH:MM:SS')
    return local_time.strftime('%Y-%m-%d %H:%M:%S')


def get_timezone(lat, lng):
    cache_key = f"timezone_{lat}_{lng}"
    timezone_data = cache.get(cache_key)

    if not timezone_data:
        api_key = settings.GOOGLE_CLOUD_API_KEY
        timestamp = int(time.time())
        url = f"https://maps.googleapis.com/maps/api/timezone/json?location={lat},{lng}&timestamp={timestamp}&key={api_key}"

        #API call
        response = requests.get(url)
        timezone_data = response.json()
        cache.set(cache_key, timezone_data, timeout = 86400)  # Cache for 24 hour

    if timezone_data['status'] == "OK":
        return timezone_data['rawOffset']
    else:
        return timezone_data['status']
