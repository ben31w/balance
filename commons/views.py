"""
Views are accessed by multiple apps or not central to a particular app.
"""

import datetime
from django.http import Http404
from django.shortcuts import render


def get_selected_date(request):
    """
    Get the date that the user submitted in an HTML date input.
    For this function to work, the date input must specify
    name="selectedDate"
    If no date is selected, load today's date by default.
    """
    # TODO GET.get formats date as  YYYY-mm-dd
    # today() formats date as       Month. dd, YYYY
    selected_date = request.GET.get("selectedDate")
    if not selected_date:
        selected_date = datetime.date.today()
    return selected_date


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