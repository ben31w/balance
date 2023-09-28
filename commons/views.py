"""
Views for the app Commons.
"""

from django.shortcuts import render


def index(request):
    """Open the home page"""
    return render(request, 'commons/index.html')
