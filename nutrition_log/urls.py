"""
URL configurations for the Nutrition Log app.
"""
from django.urls import path

from . import views

app_name = 'nutrition_log'

urlpatterns = [
    path('', views.index, name='index'),
    path('daily', views.daily, name='daily'),
    path('delete_weight/<int:dw_id>/', views.delete_weight, name='delete_weight'),
    path('set_weight', views.set_weight, name='set_weight'),
]
