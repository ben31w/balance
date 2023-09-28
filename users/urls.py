"""
URL configuration for Users app.
Users app manages log in, log out, and registration
"""
from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    # Default Django auth urls include login/ and logout/
    #  No need to have views for these patterns; Django handles this.
    #  Just need HTML file inside the templates/registration/ directory
    path('', include('django.contrib.auth.urls')),
    # Path for registration page
    path('register/', views.register, name='register'),
]