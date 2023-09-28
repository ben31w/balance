"""
URL configuration for the app Commons.
This app contains the common content that will be shared across all the apps.
"""
from django.urls import path

from . import views

app_name = 'commons'

urlpatterns = [
    path('', views.index, name='index'),
]
