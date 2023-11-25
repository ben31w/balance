"""
URL configurations for the Workout Designer app.
"""
from django.urls import path

from . import views

app_name = 'workout_designer'

urlpatterns = [
    path('', views.index, name='index'),
    path('routine/<int:routine_id>/', views.routine, name='routine'),
    path('delete_routine<int:routine_id>/', views.delete_routine, name='delete_routine'),
    path('create_workout/', views.create_workout, name='create_workout'),
]
