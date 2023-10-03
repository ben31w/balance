"""
Views for the Workout Log app.
"""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import SetForm
from .models import Set


@login_required
def index(request):
    """Load the Workout Log home page."""
    sets = Set.objects.filter(logged_by=request.user)
    dates = []
    for s in sets:
        date = s.date
        if date not in dates:
            dates.append(date)
    dates.sort(reverse=True)
    context = {'sets': sets, 'dates': dates}
    return render(request, 'workout_log/index.html', context)


@login_required()
def new_set(request):
    """Load a page where a user can log a new set"""
    if request.method == 'GET':
        form = SetForm()
    elif request.method == 'POST':
        form = SetForm(data=request.POST)
        if form.is_valid():
            this_set = form.save(commit=False)
            this_set.logged_by = request.user
            this_set.save()
            return redirect('workout_log:index')
    context = {'form': form}
    return render(request, 'workout_log/new_set.html', context)


@login_required()
def edit_set(request, set_id):
    """Load a page where a user can edit a set"""
    set = Set.objects.get(id=set_id)
    owner = set.logged_by
    verify_user_is_owner(owner, request.user)

    # Load form prefilled with data from this set (instance=set)
    if request.method == 'GET':
        form = SetForm(instance=set)
    elif request.method == 'POST':
        form = SetForm(instance=set, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('workout_log:index')
    context = {'form': form}
    return render(request, 'workout_log/edit_set.html', context)


def verify_user_is_owner(owner, user):
    """
    Users should only be able to access pages they own (i.e., pages with their
    data). If the user and page owner don't match, return an error 404 when
    the user tries to access the page.
    """
    if owner != user:
        raise Http404
