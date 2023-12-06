"""
Views are accessed by multiple apps or not central to a particular app.
"""

import datetime
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse


def get_date_url(destination_url, date):
    """
    Given a URL and a date object to send to the URL, return the URL with
    the date as a parameter.
    """
    dateStr = date.strftime('%Y-%m-%d')
    return reverse(destination_url) + f"?selectedDate={dateStr}"


def get_selected_date(request):
    """
    Get the date that the user submitted in an HTML date input.
    For this function to work, the date input must specify
    name="selectedDate"
    If no date is selected, load today's date by default.
    """
    selected_date_str = request.GET.get("selectedDate")
    if selected_date_str:
        return datetime.datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    return datetime.date.today()


def index(request):
    """Open the home page"""
    td = datetime.date.today()
    context = {'today': td}
    return render(request, 'commons/index.html', context)


def verify_user_is_owner(owner, user):
    """
    Users should only be able to access pages they own (i.e., pages with their
    data). If the user and page owner don't match, return an error 404 when
    the user tries to access the page.
    """
    if owner != user:
        raise Http404