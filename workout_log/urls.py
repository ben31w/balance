"""
URL configurations for the Workout Log app.
"""
from django.urls import path

from . import views

app_name = 'workout_log'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_set/', views.new_set, name='new_set'),
    path('edit_set/<int:set_id>/', views.edit_set, name='edit_set'),
    path('delete_set/<int:set_id>/', views.delete_set, name='delete_set'),
    path('weekly/', views.weekly, name='weekly'),
    path('charts/', views.charts, name='charts'),
    path('charts/<int:user_id>-<int:exercise_id>', views.charts_instance, name='charts_instance'),
]
