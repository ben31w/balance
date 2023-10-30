"""
Views for the app Commons.
"""

from django.http import Http404
from django.shortcuts import render


def index(request):
    """Open the home page"""
    return render(request, 'commons/index.html')


def verify_user_is_owner(owner, user):
    """
    Users should only be able to access pages they own (i.e., pages with their
    data). If the user and page owner don't match, return an error 404 when
    the user tries to access the page.
    """
    if owner != user:
        raise Http404