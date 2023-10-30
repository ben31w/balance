from datetime import date

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from commons.views import verify_user_is_owner
from .forms import DailyWeightForm
from .models import DailyWeight


@login_required
def daily(request):
    """Load the daily page for the Nutrition Log"""
    daily_weights = DailyWeight.objects.filter(user=request.user)
    json_weights = serializers.serialize("json", daily_weights)

    context = {'daily_weights': daily_weights, 'json_weights': json_weights}
    return render(request, 'nutrition_log/daily.html', context)


@login_required
def delete_weight(request, dw_id):
    """Delete this daily weight"""
    dw = DailyWeight.objects.get(id=dw_id)
    owner = dw.owner
    verify_user_is_owner(owner, request.user)
    dw.delete()
    return redirect('nutrition_log:daily')


@login_required
def index(request):
    """"Load the summary/home page for the Nutrition Log"""
    return render(request, 'nutrition_log/index.html')


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

