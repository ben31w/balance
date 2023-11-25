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
    path('edit_logged_food_item/<int:lfi_id>/', views.edit_logged_food_item, name='edit_logged_food_item'),
    path('delete_logged_food_item/<int:lfi_id>/', views.delete_logged_food_item, name='delete_logged_food_item'),
    path('weekly', views.weekly, name='weekly'),
    path('charts', views.charts, name='charts'),
    path('charts/bodyweight', views.create_weight_chart, name='create_weight_chart'),
    path('charts/calories', views.create_calories_chart, name='create_calories_chart'),
    path('set_target_calories', views.set_target_calories, name='set_target_calories'),
]
