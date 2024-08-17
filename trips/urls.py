from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('trips', views.trips, name='trips'),
    path("add-trip", views.add_trip, name="add_trip"),
    path('upcoming-trips', views.upcoming_trips, name='upcoming_trips'),
    path('previous-trips', views.previous_trips, name='previous_trips'),
]