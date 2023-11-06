from datetime import date

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from .forms import DailyWeightForm, LogFoodItemForm
from .models import DailyWeight


@login_required
def daily(request):
    """Load the daily page for the Nutrition Log"""
    daily_weights = DailyWeight.objects.filter(user=request.user)
    json_weights = serializers.serialize("json", daily_weights)

    context = {'daily_weights': daily_weights, 'json_weights': json_weights}
    return render(request, 'nutrition_log/daily.html', context)


@login_required
def index(request):
    """"Load the summary/home page for the Nutrition Log"""
    return render(request, 'nutrition_log/index.html')


@login_required
def log_food_item(request):
    """Load a form where the user can log a food item"""
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
    daily_weights = DailyWeight.objects.filter(user=request.user).order_by("date")
    if len(daily_weights) == 0:
        context = {'daily_weights': daily_weights}
        return render(request, 'nutrition_log/weekly.html', context)
    
    first_entry = daily_weights[0]
    first_date = first_entry.date
    print(first_date)

    start_date = date(2023, 10, 22)
    dates = [start_date]
    day = start_date.day
    for i in range(1, 7):
        # try-except if the day is past the month.
        d = date(2023, 10, day + i)
        dates.append(d)
    print(dates)
    context = {'daily_weights': daily_weights, 'dates': dates}
    return render(request, 'nutrition_log/weekly.html', context)

