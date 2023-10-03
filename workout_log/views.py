"""
Views for the Workout Log app.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SetForm
from .models import Exercise, Set


@login_required
def index(request):
    """Load the Workout Log home page."""
    sets = Set.objects.filter(logged_by=request.user)#.order_by("-date")
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

    exercises = Exercise.objects.all().order_by('name')
    context = {'exercises': exercises, 'form': form}
    return render(request, 'workout_log/new_set.html', context)
