from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *

# Create your views here.
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
    trip_type = request.GET.get('type', 'upcoming')
    if trip_type == 'previous':
        return HttpResponseRedirect(reverse('previous_trips'))
    return HttpResponseRedirect(reverse('upcoming_trips'))


@login_required
def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)

        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            location_id = request.POST.get('location')
            trip.location = Location.objects.get(id = location_id)
            trip.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "trips/add_trip.html", {
                "form": form
            })

    return render(request, 'trips/add_trip.html', {
        "form": TripForm()
    })


@login_required
def upcoming_trips(request):
    # Retrieve and display upcoming trips
    return render(request, 'trips/upcoming_trips.html')


@login_required
def previous_trips(request):
    # Retrieve and display previous trips
    return render(request, 'trips/previous_trips.html')