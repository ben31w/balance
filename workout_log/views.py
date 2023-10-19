"""
Views for the Workout Log app.
"""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
import plotly.graph_objects as go

from .forms import SetForm, VolumeManagerForm
from .models import Exercise, Muscle, MuscleWorked, Set

EXERCISES = Exercise.objects.order_by("name")
MUSCLES = Muscle.objects.order_by("name")
MUSCLES_WORKED = MuscleWorked.objects.all()


def calculate_volume(user, start_date, end_date):
    """
    Get this user's volume (sets per muscle) from the given start date to the
    end date. Return as a dictionary.
    :param user:
    :param start_date:
    :param end_date:
    :return: volume_dict, maps muscles to [composite, direct, indirect volume]
    """
    sets = (Set.objects.filter(logged_by=user)
            .filter(date__gte=start_date)
            .filter(date__lte=end_date))
    # Key: muscle
    # Value: 3-list [composite, direct, indirect volume]
    volume_dict = {muscle.name: [0, 0, 0] for muscle in MUSCLES}
    for set in sets:
        muscles_worked = MUSCLES_WORKED.filter(exercise=set.exercise)
        for muscle_worked in muscles_worked:
            m = muscle_worked.muscle.name
            if muscle_worked.directlyTargets:
                # update composite and direct volume
                volume_dict[m][0] += 1
                volume_dict[m][1] += 1
            else:
                # update composite and indirect volume
                volume_dict[m][0] += 0.5
                volume_dict[m][2] += 1
    return volume_dict


@login_required()
def charts(request):
    """Load a page where a user can select an exercise to view charts for"""
    context = {'exercises': EXERCISES, 'user': request.user}
    return render(request, 'workout_log/charts.html', context)


@login_required()
def charts_instance(request, user_id, exercise_id):
    """Load a chart page for the given exercise"""
    exercise = EXERCISES.get(id=exercise_id)
    sets = Set.objects.filter(logged_by=user_id).filter(exercise=exercise)
    # dates: x-axis
    dates = []
    for s in sets:
        date = s.date
        if date not in dates:
            dates.append(date)
    # weights: y-axis
    # hover_data: formatted strings that display the sets for that date
    weights = []
    hover_data = []
    for date in dates:
        sum_wt = 0
        this_dates_sets = sets.filter(date=date)
        sets_str = ""
        for s in this_dates_sets:
            reps = s.reps
            wt = s.weight
            wt_moved = reps * wt
            sum_wt += wt_moved
            sets_str += f"{wt_moved:.1f} ({reps}x{wt}), "
        avg_wt = sum_wt / len(this_dates_sets)
        weights.append(avg_wt)
        hover_data.append(sets_str)

    # return w/o creating a chart if the user hasn't logged any sets for this exercise
    if len(dates) == 0 or len(weights) == 0:
        context = {'exercise': exercise}
        return render(request, 'workout_log/charts_instance.html', context)

    fig = go.Figure(go.Scatter(
        x=dates,
        y=weights,
        hovertemplate='Date: %{x} <br>Weight: %{y:.1f} <br>Sets: %{text}',
        text=[hover_data[i] for i in range(len(hover_data))]
    ))
    fig.update_layout(
        title=f"{exercise.name} - Progressive Overload",
        xaxis_title='Date',
        yaxis_title='Average weight moved per set')
    # file arg is relative to 'balance/'
    fig.write_html(file=f"workout_log/templates/charts/{user_id}-{exercise_id}",
                   include_plotlyjs='cdn')
    # template_name arg is relative to 'balance/workout_log/templates/'
    return render(request, f'charts/{user_id}-{exercise_id}')


@login_required()
def delete_set(request, set_id):
    """Delete this set"""
    set = Set.objects.get(id=set_id)
    owner = set.logged_by
    verify_user_is_owner(owner, request.user)
    set.delete()
    return redirect('workout_log:index')


@login_required()
def edit_set(request, set_id):
    """Load a page where a user can edit a set"""
    set = Set.objects.get(id=set_id)
    owner = set.logged_by
    verify_user_is_owner(owner, request.user)

    if request.method == 'POST':
        form = SetForm(instance=set, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('workout_log:index')
    else:
        form = SetForm(instance=set)
    context = {'form': form, 'set': set}
    return render(request, 'workout_log/edit_set.html', context)


@login_required
def index(request):
    """Load the Workout Log home page (Daily view)."""
    sets = Set.objects.filter(logged_by=request.user).order_by("index")
    dates = []
    for s in sets:
        date = s.date
        if date not in dates:
            dates.append(date)
    dates.sort(reverse=True)
    context = {'sets': sets, 'dates': dates}
    return render(request, 'workout_log/index.html', context)


@login_required()
def journal(request):
    """Load the Workout Log Journal page."""
    sets = Set.objects.filter(logged_by=request.user).order_by("date")
    # keys = dates. values = dictionary that maps exercises to sets.
    # ex:
    # "Oct 16": {
    #               "Squats": [set,set,set,set]
    #               "Calf raises": [set,set,set]
    #           }
    # "Oct 15": {
    #               "Bench press": [set,set,set]
    #           }
    date_dict = dict()
    for s in sets:
        date = s.date
        if date not in date_dict.keys():
            date_dict[f"{date}"] = dict()
    for s in sets:
        date = s.date
        exercise = s.exercise
        exercise_dict = date_dict[f"{date}"]
        if exercise.__str__() not in exercise_dict.keys():
            exercise_dict[f"{exercise}"] = [s]
        else:
            exercise_dict[f"{exercise}"].append(s)

    context = {'sets': sets, 'date_dict': date_dict}
    return render(request, 'workout_log/journal.html', context)


@login_required()
def new_set(request, set_id):
    """
    Load a page where a user can log a new set.
    Parameter set_id is used to pre-populate the new set form with data
    from an existing set. This is a convenience feature to support the
    'save and log another' button. Note: if the user is adding a new set
    independent of other sets, then set_id is arbitrarily set to 0.
    """
    # Verify user owns the set that is populating this form
    if set_id != 0:
        set = Set.objects.get(id=set_id)
        owner = set.logged_by
        verify_user_is_owner(owner, request.user)

    # GET requests, initialize form without submitting
    if request.method != 'POST' and set_id == 0:
        form = SetForm()
    elif request.method != 'POST' and set_id != 0:
        form = SetForm(instance=set)
    # POST request, check if data is valid and submit
    else:
        if set_id == 0:
            form = SetForm(data=request.POST)
        else:
            form = SetForm(data=request.POST, instance=set)

        if form.is_valid():
            this_set = form.save(commit=False)
            this_set.logged_by = request.user
            this_date = form.cleaned_data["date"]
            sets = Set.objects.filter(logged_by=request.user).filter(date=this_date)
            # insert set behind all existing sets on this date by default
            this_set.index = len(sets)
            this_set.save()

            # if the user hits submit, redirect to workout log.
            # if user hits submit + log again, this block is skipped
            if "submit" in request.POST:
                return redirect('workout_log:index')

    context = {'form': form, 'set_id': set_id}
    return render(request, 'workout_log/new_set.html', context)


def verify_user_is_owner(owner, user):
    """
    Users should only be able to access pages they own (i.e., pages with their
    data). If the user and page owner don't match, return an error 404 when
    the user tries to access the page.
    """
    if owner != user:
        raise Http404


@login_required()
def volume(request):
    """Load the Volume Manager page"""
    # TODO maybe this can be changed to GET, since it isn't updating the
    #  state the of the database.
    if request.method == 'POST':
        form = VolumeManagerForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            volume_dict = calculate_volume(request.user, start_date, end_date)
            context = {
                'form': form,
                'start_date': start_date,
                'end_date': end_date,
                'volume_dict': volume_dict
            }
            return render(request, 'workout_log/volume.html', context)
    else:
        form = VolumeManagerForm()

    context = {'form': form}
    return render(request, 'workout_log/volume.html', context)


