import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from .forms import DailyWeightForm, LogFoodItemForm
from .models import DailyWeight, FoodItem, LoggedFoodItem, Unit


UNITS = Unit.objects.all()


@login_required
def daily(request):
    """Load the daily page for the Nutrition Log"""
    return render(request, 'nutrition_log/daily.html')


@login_required
def filter_nutrition_log(request):
    """
    This function is called when the user submits a new date in the datepicker.
    Get the relevant information for this date that should be rendered, and
    pass it to daily.html
    Info to pass includes the user's daily weight, total calories, etc.
    """
    daily_weights = DailyWeight.objects.filter(user=request.user)
    logged_food_items = LoggedFoodItem.objects.filter(user=request.user)
    
    selected_date = request.GET.get('selectedDate')
    if not selected_date:
        # update to better handling later.
        return render(request, 'nutrition_log/daily.html')

    # Get the daily weight
    try:
        daily_weight = daily_weights.get(date=selected_date).weight
        print(daily_weight)
    except ObjectDoesNotExist:
        daily_weight = "---"
        print(daily_weight)
    
    # Get the relevant logged food items for the selected date, 
    #  and store them as strings that can be rendered in HTML later.
    #  string format: 'Chicken breast (raw), 1x100g'
    # Also store the calories of each food item the user has logged.
    # Not currently doing much with calories list, just getting the sum
    # but it may be useful to keep this in a separate list for rendering purposes later
    relevant_items = []
    calories_list = []
    protein_list = []
    for logged_food_item in logged_food_items:
        # for some reason, this comparison only works when the dates are
        #  casted as strings.
        if str(logged_food_item.date) == str(selected_date):
            unit = UNITS.get(id=logged_food_item.unit.id)
            quantity = logged_food_item.quantity

            calories = quantity * unit.calsPerUnit
            calories_list.append(calories)

            protein = quantity * unit.proPerUnit
            protein_list.append(protein)
            
            lfi_str = f"{logged_food_item.food_item.name}, {quantity}x{unit.name}  |  {calories} Calories | {protein}g Protein"
            relevant_items.append(lfi_str)
            
    total_calories = sum(calories_list)
    total_protein = sum(protein_list)
    

    context = {
        'daily_weight': daily_weight, 
        'logged_food_items': relevant_items, 
        'total_calories': total_calories,
        'total_protein': total_protein
    }
    return render(request, 'nutrition_log/daily.html', context)


@login_required
def filter_progress_table(request):
    """
    This function is called when the user submits a start and end date in 
    the Weekly/Progress page.
    """
    start_str = request.GET.get('startDate')
    end_str = request.GET.get('endDate')

    # Error checking for start and end date inputs
    if not start_str or not end_str:
        alert = "You must fill out both a start date and an end date"
        context = {'alert': alert}
        return render(request, 'nutrition_log/weekly.html', context)
    elif end_str < start_str:
        alert = "End date must be after start date"
        context = {'alert': alert}
        return render(request, 'nutrition_log/weekly.html', context)

    # Get dates between start and end date as date objects
    start_date = datetime.datetime.strptime(start_str, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_str, '%Y-%m-%d').date()
    dates = get_list_of_dates(start_date, end_date)
    
    # Get Daily Weights logged between start and end date, inclusive
    daily_weights = DailyWeight.objects.filter(user=request.user).filter(
        date__range=[f"{start_str}", f"{end_str}"])
    
    # Return early if there are no daily weights logged
    if len(daily_weights) == 0:
        alert = "You haven't logged any weights for these dates yet"
        context = {'alert': alert}
        return render(request, 'nutrition_log/weekly.html', context)
    
    # Get average
    sumWt = 0
    for dw in daily_weights:
        sumWt += dw.weight
    avgWt = sumWt / len(daily_weights)

    context = {'daily_weights': daily_weights, 'dates': dates, 'avgWt': round(avgWt, 2)}
    return render(request, 'nutrition_log/weekly.html', context)


def get_list_of_dates(start, end):
    """
    Get list of dates between the start date and end date (inclusive).
    """
    delta_in_days = (end - start).days
    dates = [start]
    for i in range(1, delta_in_days + 1):
        d = start + relativedelta(days=i)
        dates.append(d)
    return dates


@login_required
def index(request):
    """"Load the summary/home page for the Nutrition Log"""
    return render(request, 'nutrition_log/index.html')


@login_required
def log_food_item(request):
    """Load a form where the user can log a food item"""
    if request.method == 'POST':
       form = LogFoodItemForm(data=request.POST)
       logged_food_item = form.save(commit=False)
       logged_food_item.user = request.user
       logged_food_item.save()
       return redirect('nutrition_log:daily')
    else:
        form = LogFoodItemForm()
    context = {'form': form}
    return render(request, 'nutrition_log/log_food_item.html', context)


@login_required
def set_weight(request):
    """Load a page where user can enter their daily weight"""
    if request.method == 'POST':
        form = DailyWeightForm(data=request.POST)
        if form.is_valid():
            new_weight = form.save(commit=False)
            # Before saving this instance, we need to check if an instance with
            #  this date already exists. If one already exists, update the 
            #  existing entry instead of creating a duplicate.
            try:
                old_weight = DailyWeight.objects.filter(user=request.user).get(date=new_weight.date)
                # An instance with this date exists, so edit it
                
                # If the user entered 0, they are trying to remove the weight they entered
                if new_weight.weight == 0:
                    old_weight.delete()
                    return redirect('nutrition_log:daily')
                
                # Otherwise update the weight
                old_weight.weight = new_weight.weight
                old_weight.save()
                return redirect('nutrition_log:daily')
            except ObjectDoesNotExist:
                # No instance with this date exists, so we're good to make one!
                new_weight.user = request.user
                new_weight.save()
                return redirect('nutrition_log:daily')
    else:
        form = DailyWeightForm()
    context = {'form': form}
    return render(request, 'nutrition_log/set_weight.html', context)


@login_required
def weekly(request):
    """Load the weekly page"""
    alert = ('Enter a start and end date, and press submit to view your calories '
              'and weight between those dates')
    context = {'alert': alert}
    return render(request, 'nutrition_log/weekly.html', context)

