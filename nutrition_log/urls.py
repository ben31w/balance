"""
URL configurations for the Nutrition Log app.
"""
from django.urls import path

from . import views

app_name = 'nutrition_log'

urlpatterns = [
    path('', views.index, name='index'),
]
