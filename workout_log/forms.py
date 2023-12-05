"""
List of forms for the Workout Log app.
This file defines the fields that the forms use.
The backend processing is done in views.py
"""

from django import forms

from .models import Set


class SetForm(forms.ModelForm):
    """Form where users can log a set"""
    class Meta:
        model = Set
        # TODO the exercises need to be re-orded to appear alphabetically
        # This can probably be done with formsets:
        # https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/
        fields = ['exercise', 'reps', 'weight']


class VolumeManagerForm(forms.Form):
    """
    Form on where the user can adjust the start and end dates for the Volume
    Manager
    """
    start_date = forms.DateField(label="Start date")
    end_date = forms.DateField(label="End date")
