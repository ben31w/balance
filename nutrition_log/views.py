import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
import plotly.express as px

from commons.views import get_date_url, get_selected_date, verify_user_is_owner
from .forms import DailyWeightForm, LogFoodItemForm, TargetCaloriesForm
from .models import DailyWeight, LoggedFoodItem, Unit


UNITS = Unit.objects.all()


@login_required
def index(request):
    """Load the summary/home page for the Nutrition Log"""
    # Info to get for the home page: target calories, weekly average body weight,
    #  target protein based on current weight.
    targetCals = get_target_calories(request)
    weeklyAvg = get_curr_weekly_weight(request)
    targetPro = get_target_protein(weeklyAvg)
    
    context = {'targetCals': targetCals, 'weeklyAvg': weeklyAvg, 'targetPro': targetPro}
    return render(request, "nutrition_log/index.html", context)


def get_target_calories(request):
    """Get the user's target calories or return 0 if it's unspecified"""
    try:
        targetCals = request.user.goals.target_calories
    except ObjectDoesNotExist:
        targetCals = 0
    return targetCals


def get_curr_weekly_weight(request):
    """
    Get the user's average body weight for the current week.
    Return 0 if the user hasn't logged anything.
    """
    curr_date = datetime.date.today()
    curr_weekday = curr_date.isoweekday()
    sunday = datetime.date(curr_date.year, curr_date.month, curr_date.day - curr_weekday)

    weekly_weights = DailyWeight.objects.filter(user=request.user).filter(
        date__range=[f"{sunday}", f"{curr_date}"]
    )
    return round(get_avg_weight(weekly_weights), 2)


def get_target_protein(curr_weight):
    """
    Given the user's current weight, return their target protein for the day.
    """
    # TODO this calculation doesn't work for people with high body fat. 
    #  There should be a different method for these people.
    return round(curr_weight * 0.75, 2)


def set_target_calories(request):
    """Load a page where a user can enter their target calories"""
    if request.method == "POST":
        form = TargetCaloriesForm(data=request.POST)
        if form.is_valid():
            new_target = form.save(commit=False)
            # Check if an instance already exists. Delete if so.
            #  TODO A better scheme would probably be to set each user's default to 0.
            try:
                old_goals = request.user.goals
                old_goals.delete()
            finally:
                new_target.user = request.user
                new_target.save()
                return redirect("nutrition_log:index")
    else:
        form = TargetCaloriesForm()
    context = {"form": form}
    return render(request, "nutrition_log/set_target_calories.html", context)


@login_required
def daily(request):
    """Load the daily page for the Nutrition Log"""
    date = get_selected_date(request)
    daily_wt = get_daily_weight(request, date)
    lfis, lfi_strings, calories, protein = get_logged_food_items_stats(request, date)

    # ZIP so both items can be access in the same loop in the template
    lfi_info = zip(lfis, lfi_strings)

    context = {
        "date": date,
        "daily_weight": daily_wt,
        "logged_food_items": lfi_info,
        "total_calories": calories,
        "total_protein": protein,
    }
    return render(request, "nutrition_log/daily.html", context)


@login_required
def log_food_item(request):
    """Load a form where the user can log a food item"""
    if request.method == "POST":
        form = LogFoodItemForm(data=request.POST)
        logged_food_item = form.save(commit=False)
         # for now, we'll set meal=1 (breakfast) and won't worry about lunch, dinner, and snacks.
        logged_food_item.meal = 1
        logged_food_item.user = request.user
        logged_food_item.save()

        # if the user hits submit, redirect to nutrition log.
        # if user hits submit + log again, this block is skipped
        if "submit" in request.POST:
            url = get_date_url('nutrition_log:daily', form.cleaned_data['date'])
            return redirect(url)
    else:
        form = LogFoodItemForm()
    context = {"form": form}
    return render(request, "nutrition_log/log_food_item.html", context)


@login_required()
def edit_logged_food_item(request, lfi_id):
    """Load a page where a user can edit a logged food item"""
    lfi = LoggedFoodItem.objects.get(id=lfi_id)
    owner = lfi.user
    verify_user_is_owner(owner, request.user)

    if request.method == 'POST':
        form = LogFoodItemForm(instance=lfi, data=request.POST)
        if form.is_valid():
            form.save()
            url = get_date_url('nutrition_log:daily', form.cleaned_data['date'])
            return redirect(url)
    else:
        form = LogFoodItemForm(instance=lfi)
    context = {'form': form, 'lfi': lfi}
    return render(request, 'nutrition_log/edit_logged_food_item.html', context)


@login_required
def delete_logged_food_item(request, lfi_id):
    """Delete this logged food item"""
    lfi = LoggedFoodItem.objects.get(id=lfi_id)
    owner = lfi.user
    verify_user_is_owner(owner, request.user)
    lfi.delete()
    url = get_date_url('nutrition_log:daily', lfi.date)
    return redirect(url)


@login_required
def set_weight(request):
    """Load a page where user can enter their daily weight"""
    if request.method == "POST":
        form = DailyWeightForm(data=request.POST)
        if form.is_valid():
            new_weight = form.save(commit=False)
            # Before saving this instance, we need to check if an instance with
            #  this date already exists. If one already exists, update the
            #  existing entry instead of creating a duplicate.
            try:
                old_weight = DailyWeight.objects.filter(user=request.user).get(
                    date=new_weight.date
                )
                # An instance with this date exists, so edit it

                # If the user entered 0, they are trying to remove the weight they entered
                if new_weight.weight == 0:
                    old_weight.delete()
                # Otherwise update the weight
                else:
                    old_weight.weight = new_weight.weight
                    old_weight.save()
            except ObjectDoesNotExist:
                # No instance with this date exists, so we're good to make one!
                new_weight.user = request.user
                new_weight.save()
            finally:
                url = get_date_url('nutrition_log:daily', form.cleaned_data['date'])
                return redirect(url)
    else:
        form = DailyWeightForm()
    context = {"form": form}
    return render(request, "nutrition_log/set_weight.html", context)


def get_daily_weight(request, date):
    """Get daily weight for the given date. Or return '---' if there is none."""
    daily_weights = DailyWeight.objects.filter(user=request.user)
    try:
        daily_weight = daily_weights.get(date=date).weight
    except ObjectDoesNotExist:
        daily_weight = "---"
    return daily_weight


def get_logged_food_items_stats(request, date):
    """
    Search through the user's logged food items for this date.
    Return four things:
        - list of logged food item objects
        - list of logged food item strings that can be rendered in HTML later.
        - total calories
        - total protein
    """
    strings = []
    calories_list = []
    protein_list = []

    logged_food_items = LoggedFoodItem.objects.filter(user=request.user).filter(date=date)
    for logged_food_item in logged_food_items:
        unit = UNITS.get(id=logged_food_item.unit.id)
        quantity = logged_food_item.quantity

        calories = quantity * unit.calsPerUnit
        calories_list.append(calories)

        protein = quantity * unit.proPerUnit
        protein_list.append(protein)

        lfi_str = f"{logged_food_item} | {calories} Calories | {protein}g Protein"
        strings.append(lfi_str)
    total_calories = sum(calories_list)
    total_protein = sum(protein_list)

    return logged_food_items, strings, total_calories, total_protein


@login_required
def weekly(request):
    """Load the weekly page"""
    start_date_str = request.GET.get("startDate")
    end_date_str = request.GET.get("endDate")

    # Verify start date and end date are valid.
    if not start_date_str or not end_date_str:
        alert = "You must fill out both a start date and an end date"
        context = {"alert": alert}
        return render(request, "nutrition_log/weekly.html", context)
    elif end_date_str < start_date_str:
        alert = "End date must be after start date"
        context = {"alert": alert}
        return render(request, "nutrition_log/weekly.html", context)

    dates = get_list_of_dates(start_date_str, end_date_str)
    actual_daily_weights = DailyWeight.objects.filter(user=request.user).filter(
        date__range=[f"{start_date_str}", f"{end_date_str}"]
    )
    padded_daily_weights = get_padded_daily_weights(dates, actual_daily_weights)
    avgWt = get_avg_weight(actual_daily_weights)
    daily_calories = get_list_of_calories(request, dates)
    avgCal = get_avg_calories(request, dates)  # Django doesn't like avg_name

    # zip these lists so they can be used more efficiently in the template
    lists = zip(dates, padded_daily_weights, daily_calories)
    context = {
        "lists": lists,
        "avgWt": round(avgWt, 2),
        "avgCal": round(avgCal, 2),
    }
    return render(request, "nutrition_log/weekly.html", context)


def get_avg_weight(daily_weights):
    """Get avg daily weight from a queryset of daily weights"""
    if len(daily_weights) == 0:
        return 0
    sumWt = 0
    for dw in daily_weights:
        sumWt += dw.weight
    return sumWt / len(daily_weights)


def get_padded_daily_weights(dates, actual_daily_weights):
    """
    Get list of daily weights for these dates.
    However, if there is a date without a weight, insert '---' as filler
    """
    return_weights = []
    for date in dates:
        try:
            dw = actual_daily_weights.get(date=date)
            return_weights.append(dw.weight)
        except ObjectDoesNotExist:
            return_weights.append("---")
    return return_weights


def get_list_of_calories(request, dates):
    """Get a list of the user's calories for these dates"""
    calories_list = []
    for date in dates:
        _,_, daily_calories, _ = get_logged_food_items_stats(request, date)
        calories_list.append(daily_calories)
    return calories_list


def get_list_of_dates(start_date_str, end_date_str):
    """
    Get list of dates between the start date and end date (inclusive).
    """
    start = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

    delta_in_days = (end - start).days
    dates = [start]
    for i in range(1, delta_in_days + 1):
        d = start + relativedelta(days=i)
        dates.append(d)
    return dates


def get_avg_calories(request, dates):
    """Get average calories for these dates"""
    total_cals = 0
    for date in dates:
        _,_, daily_calories, _ = get_logged_food_items_stats(request, date)
        total_cals += daily_calories
    return total_cals / len(dates)


@login_required
def charts(request):
    """Load the charts page"""
    return render(request, 'nutrition_log/charts.html')


def create_chart(x_pts, y_pts, x_label, y_label, title, filepath):
    """
    Create a line chart with the given data and filepath.
    Note:
    filepath arg is relative to 'balance/' 
    while the arg for render() is relative to 'balance/nutrition_log/templates/'
    """
    fig = px.scatter(x=x_pts, y=y_pts, labels={"x": x_label, "y": y_label}, title=title)
    fig.write_html(file=f"nutrition_log/templates/{filepath}")


@login_required
def create_calories_chart(request):
    """Create a daily calories vs time chart for the user, and load a page to display it"""
    logged_food_items = LoggedFoodItem.objects.filter(user=request.user).order_by("date")
    if len(logged_food_items) == 0:
        alert = "You haven't logged any food items yet."
        context = {'alert': alert}
        return render(request, "nutrition_log/charts.html", context)
    
    # Get dates
    dates = []
    for lfi in logged_food_items:
        if lfi.date not in dates:
            dates.append(lfi.date)
    # Get calories for each date
    calories_list = []
    for date in dates:
        _,_, calories, _ = get_logged_food_items_stats(request, date=date)
        calories_list.append(calories)

    # Create and render chart
    title = "Calorie Intake Over Time"
    filename = f"charts/{request.user}-calories.html"
    create_chart(dates, calories_list, 'Date', 'Daily Calories', title, filename)
    return render(request, filename)


@login_required
def create_weight_chart(request):
    """Create a weight vs time chart for the user, and load a page to display it"""
    daily_weights = DailyWeight.objects.filter(user=request.user).order_by("date")
    if len(daily_weights) == 0:
        alert = "You haven't logged any daily weights yet."
        context = {'alert': alert}
        return render(request, "nutrition_log/charts.html", context)

    dates = [dw.date for dw in daily_weights]
    weights = [dw.weight for dw in daily_weights]
    # harder approach that would be more ideal:
    # create the line charts
    # save as HTML
    # get the div and put it inside charts?? IDK how to do this yet

    # easier approach that is actually implemented:
    # just do what the workout log does, and open the HTML directly.
    title = "Body Weight Over Time"
    filename = f"charts/{request.user}-weight.html"
    create_chart(dates, weights, 'Date', 'Weight', title, filename)
    return render(request, filename)
