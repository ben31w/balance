from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """"Load the homa page for the Nutrition Log"""
    return render(request, 'nutrition_log/index.html')
