import datetime
from random import randrange

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from workout_designer.models import Routine


@login_required
def index(request):
    """Load the My Workouts page"""
    return render(request, "workout_designer/index.html")


@login_required
def create_workout(request):
    """
    GET: Load the form for creating a workout
    POST: Process the form for creating a workout
    """
    if request.method == "POST":
        schedule = request.POST.get("schedule")
        lower_hr_str = request.POST.get("lowerLimitHrs")
        lower_min_str = request.POST.get("lowerLimitMin")
        upper_hr_str = request.POST.get("upperLimitHrs")
        upper_min_str = request.POST.get("upperLimitMin")
        lower_limit, upper_limit = get_limits(lower_hr_str, lower_min_str, upper_hr_str, upper_min_str)
        goal = request.POST.get("goal")
        split = request.POST.get("split")

        create_routine(request, schedule, upper_limit, lower_limit, split, goal)
    else:
        return render(request, 'workout_designer/create_workout.html')
    return render(request, 'workout_designer/create_workout.html')


@login_required
def create_routine(request, schedule, upper_limit, lower_limit, split, goal):
    """
    Create a Routine given these parameters
    - request : indicates the user
    - schedule : sync or async
    - upper_limit: upper workout limit in min
    - lower_limit: lower workout limit in min
    - split: Anything, Arnold, Bro, Push-Pull-Legs, Upper-Lower
    - goal: musc or fit
    """
    r = Routine()
    r.name = split
    r.date_created = datetime.date.today()
    r.user = request.user
    r.is_synchronous = schedule == "sync"
    if split == 'Anything':
        choices = [abreviation for abreviation,_ in Routine.SPLIT_CHOICES]
        rand = randrange(len(choices))
        r.split = choices[rand]
    else:
        r.split = split
    r.lower_limit_min = lower_limit
    r.upper_limit_min = upper_limit
    r.is_muscle_focused = goal == "musc"
    r.save()
    create_days_for_routine(r)


@login_required
def create_days_for_routine(routine):
    """Create days"""
    if routine.is_synchronous:
        print("yes")
    else:
        print("no")



def get_limits(lower_hr_str, lower_min_str, upper_hr_str, upper_min_str):
    """
    Given strings for lower and upper limits' hrs and min, 
    get each limit in minutes (as an int)
    """
    lower_limit = get_minutes(lower_hr_str, lower_min_str)
    upper_limit = get_minutes(upper_hr_str, upper_min_str)

    if lower_limit == 0 and upper_limit == 0:
        lower_limit = 45
        upper_limit = 75
    elif lower_limit == 0:
        lower_limit = max(upper_limit - 30, 20)
    elif upper_limit == 0:
        upper_limit = lower_limit + 30
    
    return lower_limit, upper_limit


def get_minutes(hrs, min):
    """Given strings for hrs and min, get the total min as an int"""
    total = 0
    try:
        total += int(hrs) * 60
    except ValueError:
        pass
    try:
        total += int(min)
    except ValueError:
        pass
    return total