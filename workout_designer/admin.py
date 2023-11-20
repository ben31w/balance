from django.contrib import admin

from .models import Routine, Day, PlannedSets

# Register your models here.
admin.site.register(Routine)
admin.site.register(Day)
admin.site.register(PlannedSets)