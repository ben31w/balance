from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Load the My Workouts page"""
    return render(request, "workout_designer/index.html")
