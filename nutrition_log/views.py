from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def daily(request):
    """Load the daily pafe for the Nutrition Log"""
    return render(request, 'nutrition_log/daily.html')


@login_required
def index(request):
    """"Load the summary/home page for the Nutrition Log"""
    return render(request, 'nutrition_log/index.html')
