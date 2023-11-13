"""
URL configurations for the Nutrition Log app.
"""
from django.urls import path

from . import views

app_name = 'nutrition_log'

urlpatterns = [
    path('', views.index, name='index'),
    path('daily', views.daily, name='daily'),
    path('set_weight', views.set_weight, name='set_weight'),
    path('log_food_item', views.log_food_item, name='log_food_item'),
    path('weekly', views.weekly, name='weekly'),
    path('filter_progress_table', views.filter_progress_table, name='filter_progress_table'),
]
