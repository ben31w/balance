"""
List of forms for the Nutrition Log app.
This file defines the fields that the forms use.
The backend processing is done in views.py
"""

from django import forms

from .models import DailyWeight


class DailyWeightForm(forms.ModelForm):
    """Form where users can log their daily weight"""
    class Meta:
        model = DailyWeight
        fields = ['weight']


