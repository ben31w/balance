import datetime
from random import randrange

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from workout_designer.models import Focus, Routine, DayType, Day, PlannedSets
from workout_log.models import MuscleWorked


@login_required
def index(request):
    """Load the My Workouts page"""
    routines = Routine.objects.filter(user=request.user)

    # Create routine dictionary with this structure:
    # {
    #    'routine 1': {
    #                     'day 1': [planned sets for exercise 1, planned sets for exercise 2, ...],
    #                     'day 2': [planned sets for exercise 1, planned sets for exercise 2, ...],
    #                     ...
    #                 },
    #    ...
    # }
    routine_dict = dict()
    for routine in routines:
        routine_dict[f"{routine}"] = dict()
        days = Day.objects.filter(routine=routine)
        for day in days:
            # need to account for two days with the same name (ex: two lower days)
            if day.__str__() in routine_dict[f"{routine}"].keys():
                curr_day_ls = routine_dict[f"{routine}"][f"{day} 2"] = []
            else:
                curr_day_ls = routine_dict[f"{routine}"][f"{day}"] = []
            planned_sets = PlannedSets.objects.filter(day=day)
            for ps in planned_sets:
                curr_day_ls.append(ps)
    context = {'routine_dict': routine_dict}
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
    r.is_muscle_focused = goal == "muscle"
    r.save()
    create_days_for_routine(r)


@login_required
def create_days_for_routine(routine):
    """Create Days for a Routine"""
    match routine.split:
        case Routine.ARN:
            create_days_arnold(routine)
        case Routine.BRO:
            create_days_bro(routine)
        case Routine.PPL:
            create_days_ppl(routine)
        case Routine.UL:
            create_days_ul(routine)


def create_days_arnold(routine):
    """Create days for an Arnold split"""
    # is it worth splitting this into sync and async?
    # is it worth storing rest days? probably not!
    # i'm just banking on these days being created and stored in order.
    if routine.is_synchronous:
        create_day(routine, "Legs M", DayType.LEGS)
        create_day(routine, "Back-Chest Tu", DayType.BC)
        create_day(routine, "Shoulders-Arms W", DayType.SA)
        create_day(routine, "Legs Th", DayType.LEGS)
        create_day(routine, "Back-Chest F", DayType.BC)
        create_day(routine, "Shoulders-Arms Sa", DayType.SA)
        create_day(routine, "Rest Su", DayType.REST)
    else:
        create_day(routine, "Legs A", DayType.LEGS)
        create_day(routine, "Back-Chest A", DayType.BC)
        create_day(routine, "Shoulders-Arms A", DayType.SA)
        create_day(routine, "Rest", DayType.REST)
        create_day(routine, "Legs B", DayType.LEGS)
        create_day(routine, "Back-Chest B", DayType.BC)
        create_day(routine, "Shoulders-Arms B", DayType.SA)
        create_day(routine, "Rest", DayType.REST)


def create_days_bro(routine):
    """Create days for a Bro split"""
    create_day(routine, "Chest", DayType.CHEST)
    create_day(routine, "Back", DayType.BACK)
    create_day(routine, "Legs", DayType.LEGS)
    create_day(routine, "Shoulders", DayType.SHOULDERS)
    create_day(routine, "Arms", DayType.ARMS)
    create_day(routine, "Rest", DayType.REST)
    create_day(routine, "Rest", DayType.REST)


def create_days_ppl(routine):
    """Create days for a PPL split"""
    if routine.is_synchronous:
        create_day(routine, "Legs M", DayType.LEGS)
        create_day(routine, "Push Tu", DayType.PUSH)
        create_day(routine, "Pull W", DayType.PULL)
        create_day(routine, "Legs Th", DayType.LEGS)
        create_day(routine, "Push F", DayType.PUSH)
        create_day(routine, "Pull Sa", DayType.PULL)
        create_day(routine, "Rest Su", DayType.REST)
    else:
        create_day(routine, "Legs A", DayType.LEGS)
        create_day(routine, "Push A", DayType.PUSH)
        create_day(routine, "Pull A", DayType.PULL)
        create_day(routine, "Rest", DayType.REST)
        create_day(routine, "Legs B", DayType.LEGS)
        create_day(routine, "Push B", DayType.PUSH)
        create_day(routine, "Pull B", DayType.PULL)
        create_day(routine, "Rest", DayType.REST)


def create_days_ul(routine):
    """Create days for a UL split"""
    create_day(routine, "Upper", DayType.UPPER)
    create_day(routine, "Lower", DayType.LOWER)
    create_day(routine, "Rest", DayType.REST)
    create_day(routine, "Upper", DayType.UPPER)
    create_day(routine, "Lower", DayType.LOWER)
    create_day(routine, "Rest", DayType.REST)
    create_day(routine, "Rest", DayType.REST)


def create_day(routine, name, day_type):
    """Create a Day for this Routine, given a name and type"""
    d = Day()
    d.routine = routine
    d.name = name
    d.day_type = DayType.objects.get(name=day_type)
    d.time_est_min = 0
    d.save()
    create_sets_for_day(routine, d)


def create_sets_for_day(routine, day):
    """Create sets for this day"""
    if day.day_type == DayType.objects.get(name=DayType.REST):
        return
    
    # Get muscles that this day works
    focii = Focus.objects.filter(day_type=day.day_type)
    muscles = [focus.muscle for focus in focii]

    # Keep addings sets as long as we're in the time limits
    curr_time_est = day.time_est_min
    while curr_time_est < routine.lower_limit_min:
        for muscle in muscles:
            ps = PlannedSets()
            
            ps.day = day

            # get random exercise that targets this muscle
            muscles_worked = MuscleWorked.objects.filter(muscle=muscle).filter(directly_targets=True)
            exercises = [mw.exercise for mw in muscles_worked]
            ps.exercise = exercises[randrange(len(exercises))]
    
            # Assume 3 sets for now.
            ps.num_sets = 3

            # Get random reps between 6 and 12, even-numbers
            ps.reps = randrange(6, 13, 2)

            # Get very rough time estimate using these rules:
            #  Compound lifts require a 2 minute warmup, and take 3.5 minutes per set.
            #  Isolation lifts require no warmup and take 2.5 minutes per set.
            #  Might want to change this calculation later to reflect reps
            if ps.exercise.is_compound:
                ps.time_est_min = 2 + ps.num_sets * 3.5
            else:
                ps.time_est_min = ps.num_sets * 2.5
            curr_time_est += ps.time_est_min
            ps.save()
            if curr_time_est > routine.lower_limit_min:
                break
    day.time_est_min = curr_time_est
    day.save()


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