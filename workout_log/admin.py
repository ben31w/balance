from django.contrib import admin

from .models import Exercise, Muscle, MuscleWorked, Set

# Register your models here.
admin.site.register(Exercise)
admin.site.register(Muscle)
admin.site.register(MuscleWorked)
admin.site.register(Set)
