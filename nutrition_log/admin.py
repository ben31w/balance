from django.contrib import admin

from .models import DailyWeight, FoodItem, Recipe, Unit, Contains, LoggedFoodItem


admin.site.register(DailyWeight)
admin.site.register(FoodItem)
admin.site.register(Recipe)
admin.site.register(Unit)
admin.site.register(Contains)
admin.site.register(LoggedFoodItem)