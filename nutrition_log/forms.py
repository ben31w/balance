"""
List of forms for the Nutrition Log app.
This file defines the fields that the forms use.
The backend processing is done in views.py
"""

from datetime import date

from django import forms

from .models import DailyWeight, LoggedFoodItem, Goals


class DailyWeightForm(forms.ModelForm):
    """Form where users can log their daily weight"""
    class Meta:
        model = DailyWeight
        fields = ['date', 'weight']
        widgets = {'date': forms.SelectDateWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today()  # Set the default date to today (temp)


class LogFoodItemForm(forms.ModelForm):
    """Form where users can log a food item"""
    class Meta:
        model = LoggedFoodItem
        fields = ['date', 'food_item', 'unit', 'quantity', 'meal']
        widgets = {'date': forms.SelectDateWidget()}


class TargetCaloriesForm(forms.ModelForm):
    """Form where users can set their target calories"""
    class Meta:
        model = Goals
        fields = ['target_calories']
