"""
Views for the Workout Log app.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Load the Workout Log home page."""
    return render(request, 'workout_log/index.html')
