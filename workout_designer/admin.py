from django.contrib import admin

from .models import Routine, DayType, Focus, Day, PlannedSets

# Register your models here.
admin.site.register(Routine)
admin.site.register(DayType)
admin.site.register(Focus)
admin.site.register(Day)
admin.site.register(PlannedSets)