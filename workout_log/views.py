"""
Views for the Workout Log app.
"""
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import SetForm, WeeklyForm
from .models import Exercise, Muscle, MuscleWorked, Set

EXERCISES = Exercise.objects.all()
MUSCLES = Muscle.objects.all()
MUSCLES_WORKED = MuscleWorked.objects.all()

@login_required
def index(request):
    """Load the Workout Log home page (Daily view)."""
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
    context = {'form': form, 'set': set}
    return render(request, 'workout_log/edit_set.html', context)


@login_required()
def weekly(request):
    """Load the Weekly View page"""
    # TODO fix this
    if request.method == 'GET':
        form = WeeklyForm()
    elif request.method == 'POST':
        form = WeeklyForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            # Calculate weekly volume
            sets = (Set.objects.filter(logged_by=request.user)
                    .filter(date__gte=start_date)
                    .filter(date__lte=end_date))
            volume_dict = {muscle.name: 0 for muscle in MUSCLES}
            for set in sets:
                muscles_worked = MUSCLES_WORKED.filter(exercise=set.exercise)
                for muscle_worked in muscles_worked:
                    if muscle_worked.directlyTargets:
                        volume_dict[muscle_worked.muscle.name] += 1
                    else:
                        volume_dict[muscle_worked.muscle.name] += 0.5

            context = {
                'form': form,
                'start_date': start_date,
                'end_date': end_date,
                'volume_dict': volume_dict
            }
            return render(request, 'workout_log/weekly.html', context)

    context = {'form': form}
    return render(request, 'workout_log/weekly.html', context)


def verify_user_is_owner(owner, user):
    """
    Users should only be able to access pages they own (i.e., pages with their
    data). If the user and page owner don't match, return an error 404 when
    the user tries to access the page.
    """
    if owner != user:
        raise Http404
