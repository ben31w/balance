from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Load the My Workouts page"""
    return render(request, "workout_designer/index.html")


@login_required
def create_workout(request):
    """Loads the form for creating a workout"""
    if request.method == "POST":
        # TODO add validation to make sure the fields are filled out.
        schedule = request.POST.get("schedule")

        lower_hr_str = request.POST.get("lowerLimitHrs")
        lower_min_str = request.POST.get("lowerLimitMin")
        upper_hr_str = request.POST.get("upperLimitHrs")
        upper_min_str = request.POST.get("upperLimitMin")
        lower_limit = get_minutes(lower_hr_str, lower_min_str)
        upper_limit = get_minutes(upper_hr_str, upper_min_str)

        goal = request.POST.get("goal")

        split = request.POST.get("split")

        print(schedule)
        print(f"Lower limit: {lower_limit}")
        print(f"Upper limit: {upper_limit}")
        print(goal)
        print(split)
    else:
        return render(request, 'workout_designer/create_workout.html')
    return render(request, 'workout_designer/create_workout.html')


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