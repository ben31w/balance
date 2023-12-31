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
        fields = ['weight']


class LogFoodItemForm(forms.ModelForm):
    """Form where users can log a food item"""
    class Meta:
        model = LoggedFoodItem
        fields = ['food_item', 'unit', 'quantity']


class TargetCaloriesForm(forms.ModelForm):
    """Form where users can set their target calories"""
    class Meta:
        model = Goals
        fields = ['target_calories']
