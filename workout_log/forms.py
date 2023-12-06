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
        fields = ['exercise', 'reps', 'weight']
    
    def __init__(self, *args, **kwargs):
        super(SetForm, self).__init__(*args, **kwargs)
        
        # Sort exercise options alphabetically
        exercise_field = self.fields['exercise']
        exercise_field.queryset = exercise_field.queryset.order_by('name')



class VolumeManagerForm(forms.Form):
    """
    Form on where the user can adjust the start and end dates for the Volume
    Manager
    """
    start_date = forms.DateField(label="Start date")
    end_date = forms.DateField(label="End date")
