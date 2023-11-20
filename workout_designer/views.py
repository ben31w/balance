import datetime
from random import randrange

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from workout_designer.models import Routine, Day


@login_required
def index(request):
    """Load the My Workouts page"""
    routines = Routine.objects.filter(user=request.user)
    routine_dict = dict()
    for routine in routines:
        routine_dict[f"{routine}"] = []
        days = Day.objects.filter(routine=routine)
        for day in days:
            routine_dict[f"{routine}"].append(day)
    context = {'routines': routines, 'routine_dict': routine_dict}
    return render(request, "workout_designer/index.html", context)


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
        return redirect('workout_designer:index')
    else:
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
    r.date_created = datetime.date.today()
    r.user = request.user
    r.is_synchronous = schedule == "sync"
    if split == 'Anything':
        choices = [abreviation for abreviation,_ in Routine.SPLIT_CHOICES]
        rand = randrange(len(choices))
        r.split = choices[rand]
    else:
        r.split = split
    r.name = r.split
    r.lower_limit_min = lower_limit
    r.upper_limit_min = upper_limit
    r.is_muscle_focused = goal == "musc"
    r.save()
    create_days_for_routine(r)


@login_required
def create_days_for_routine(routine):
    """Create Days for a Routine"""
    match routine.split:
        case 'Arnold':
            create_days_arnold(routine)
        case 'Bro':
            create_days_bro(routine)
        case 'PPL':
            create_days_ppl(routine)
        case 'UL':
            create_days_ul(routine)


def create_days_arnold(routine):
    """Create days for an Arnold split"""
    # is it worth splitting this into sync and async?
    # is it worth storing rest days? probably not!
    # i'm just banking on these days being created and stored in order.
    if routine.is_synchronous:
        create_day(routine, "Legs M", Day.LEGS)
        create_day(routine, "Back-Chest Tu", Day.BC)
        create_day(routine, "Shoulders-Arms W", Day.SA)
        create_day(routine, "Legs Th", Day.LEGS)
        create_day(routine, "Back-Chest F", Day.BC)
        create_day(routine, "Shoulders-Arms Sa", Day.SA)
        create_day(routine, "Rest Su", Day.REST)
    else:
        create_day(routine, "Legs A", Day.LEGS)
        create_day(routine, "Back-Chest A", Day.BC)
        create_day(routine, "Shoulders-Arms A", Day.SA)
        create_day(routine, "Rest", Day.REST)
        create_day(routine, "Legs B", Day.LEGS)
        create_day(routine, "Back-Chest B", Day.BC)
        create_day(routine, "Shoulders-Arms B", Day.SA)
        create_day(routine, "Rest", Day.REST)


def create_days_bro(routine):
    """Create days for a Bro split"""
    create_day(routine, "Chest", Day.CHEST)
    create_day(routine, "Back", Day.BACK)
    create_day(routine, "Legs", Day.LEGS)
    create_day(routine, "Shoulders", Day.SHOULDERS)
    create_day(routine, "Arms", Day.ARMS)
    create_day(routine, "Rest", Day.REST)
    create_day(routine, "Rest", Day.REST)


def create_days_ppl(routine):
    """Create days for a PPL split"""
    if routine.is_synchronous:
        create_day(routine, "Legs M", Day.LEGS)
        create_day(routine, "Push Tu", Day.PUSH)
        create_day(routine, "Pull W", Day.PULL)
        create_day(routine, "Legs Th", Day.LEGS)
        create_day(routine, "Push F", Day.PUSH)
        create_day(routine, "Pull Sa", Day.PULL)
        create_day(routine, "Rest Su", Day.REST)
    else:
        create_day(routine, "Legs A", Day.LEGS)
        create_day(routine, "Push A", Day.PUSH)
        create_day(routine, "Pull A", Day.PULL)
        create_day(routine, "Rest", Day.REST)
        create_day(routine, "Legs B", Day.LEGS)
        create_day(routine, "Push B", Day.PUSH)
        create_day(routine, "Pull B", Day.PULL)
        create_day(routine, "Rest", Day.REST)


def create_days_ul(routine):
    """Create days for a UL split"""
    create_day(routine, "Upper", Day.UPPER)
    create_day(routine, "Lower", Day.LOWER)
    create_day(routine, "Rest", Day.REST)
    create_day(routine, "Upper", Day.UPPER)
    create_day(routine, "Lower", Day.LOWER)
    create_day(routine, "Rest", Day.REST)
    create_day(routine, "Rest", Day.REST)


def create_day(routine, name, focus):
    """Create a Day for this Routine, given a name and focus"""
    d = Day()
    d.routine = routine
    d.name = name
    d.focus = focus
    d.time_est_min = 0
    d.save()


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