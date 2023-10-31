"""
List of forms for the Nutrition Log app.
This file defines the fields that the forms use.
The backend processing is done in views.py
"""

from datetime import date

from django import forms

from .models import DailyWeight


class DailyWeightForm(forms.ModelForm):
    """Form where users can log their daily weight"""
    class Meta:
        model = DailyWeight
        fields = ['date', 'weight']
        widgets = {'date': forms.SelectDateWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today()  # Set the default date to today (temp)
