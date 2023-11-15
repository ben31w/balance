import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
import plotly.express as px

from .forms import DailyWeightForm, LogFoodItemForm
from .models import DailyWeight, LoggedFoodItem, Unit


UNITS = Unit.objects.all()


@login_required
def index(request):
    """ "Load the summary/home page for the Nutrition Log"""
    return render(request, "nutrition_log/index.html")


@login_required
def daily(request):
    """Load the daily page for the Nutrition Log"""
    date = get_selected_date(request)
    daily_wt = get_daily_weight(request, date)
    strings, calories, protein = get_logged_food_items_stats(request, date)

    context = {
        "date": date,
        "daily_weight": daily_wt,
        "logged_food_items": strings,
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
        logged_food_item.user = request.user
        logged_food_item.save()
        return redirect("nutrition_log:daily")
    else:
        form = LogFoodItemForm()
    context = {"form": form}
    return render(request, "nutrition_log/log_food_item.html", context)


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
                return redirect("nutrition_log:daily")
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
    Return three things:
        - list of logged food item strings that can be rendered in HTML later.
        - total calories
        - total protein
    """
    strings = []
    calories_list = []
    protein_list = []

    logged_food_items = LoggedFoodItem.objects.filter(user=request.user)
    for logged_food_item in logged_food_items:
        # dates must be cast as strings for this comparison to work.
        if str(logged_food_item.date) == str(date):
            unit = UNITS.get(id=logged_food_item.unit.id)
            quantity = logged_food_item.quantity

            calories = quantity * unit.calsPerUnit
            calories_list.append(calories)

            protein = quantity * unit.proPerUnit
            protein_list.append(protein)

            lfi_str = f"{logged_food_item.food_item.name}, {quantity}x{unit.name}  |  {calories} Calories | {protein}g Protein"
            strings.append(lfi_str)
    total_calories = sum(calories_list)
    total_protein = sum(protein_list)

    return strings, total_calories, total_protein


def get_selected_date(request):
    """
    Get the date that the user submitted in the dateInput on the daily page.
    Or load today's date by default.
    """
    # TODO GET.get formats date as  YYYY-mm-dd
    # today() formats date as       Month. dd, YYYY
    selected_date = request.GET.get("selectedDate")
    if not selected_date:
        selected_date = datetime.date.today()
    return selected_date


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
    avgWt = get_avg_daily_weight(actual_daily_weights)
    daily_calories = get_list_of_calories(request, dates)

    # zip these lists so they can be used more efficiently in the template
    lists = zip(dates, padded_daily_weights, daily_calories)
    context = {
        "lists": lists,
        "avgWt": round(avgWt, 2),
    }
    return render(request, "nutrition_log/weekly.html", context)


def get_avg_daily_weight(daily_weights):
    """Get avg daily weight from queryset"""
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
        _, daily_calories, _ = get_logged_food_items_stats(request, date)
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


@login_required
def charts(request):
    """Load the charts page"""
    return render(request, 'nutrition_log/charts.html')
    

@login_required
def create_calories_chart(request):
    """Create a daily calories vs time chart for the user, and load a page to display it"""
    return


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

    fig = px.scatter(x=dates, y=weights, labels={"x": "date", "y": "weight"})
    # file arg is relative to 'balance/'
    filename = f"charts/{request.user}-weight.html"
    fig.write_html(file=f"nutrition_log/templates/{filename}", include_plotlyjs="cdn")

    # however, render's arg is relative to 'balance/nutrition_log/templates/'
    return render(request, filename)
