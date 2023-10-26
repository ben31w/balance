from datetime import date

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render

from .forms import DailyWeightForm
from .models import DailyWeight


@login_required
def daily(request):
    """Load the daily page for the Nutrition Log"""
    if request.method == 'POST':
        form = DailyWeightForm(data=request.POST)
        if form.is_valid():
            daily_weight = form.save(commit=False)
            daily_weight.date = date.today()  # temporary
            daily_weight.user = request.user
            daily_weight.save()
    else:
        form = DailyWeightForm()
    
    daily_weights = DailyWeight.objects.filter(user=request.user)
    weights_json = serializers.serialize("json", daily_weights)

    for dw in daily_weights:
        print(dw)

    context = {'form': form, 'daily_weights': weights_json}
    return render(request, 'nutrition_log/daily.html', context)


@login_required
def index(request):
    """"Load the summary/home page for the Nutrition Log"""
    return render(request, 'nutrition_log/index.html')
