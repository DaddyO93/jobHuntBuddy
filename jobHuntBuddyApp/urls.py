from jobHuntBuddyApp.views import add_position
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("user/register", views.register),
    path("user/login", views.login),
    path("success", views.main),
    path("add_position", views.add_position),
    path('add_contact_to_position', views.add_contact_to_position),
    path('position_details/<int:position_id>', views.position_details),
    ]