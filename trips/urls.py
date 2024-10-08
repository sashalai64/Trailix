from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("trips/", views.trips, name="trips"),
    path("add-trip/", views.add_trip, name="add_trip"),
    path("get-cities/", views.get_cities, name="get_cities"),
    path("edit-trip/<int:tripId>/", views.edit_trip, name="edit_trip")
]