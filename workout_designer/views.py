from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Load the My Workouts page"""
    return render(request, "workout_designer/index.html")


@login_required
def create_workout(request):
    """Loads the form for creating a workout"""
    return render(request, 'workout_designer/create_workout.html')

