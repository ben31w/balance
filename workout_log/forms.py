"""
List of forms for the Workout Log app.
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
        fields = ['date', 'exercise', 'reps', 'weight']

