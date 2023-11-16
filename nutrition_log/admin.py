from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import DailyWeight, FoodItem, Recipe, Unit, Contains, LoggedFoodItem, Goals


admin.site.register(DailyWeight)
admin.site.register(FoodItem)
admin.site.register(Recipe)
admin.site.register(Unit)
admin.site.register(Contains)
admin.site.register(LoggedFoodItem)

# Define an inline admin descriptor for Goals model
class GoalsInline(admin.StackedInline):
    model = Goals
    can_delete = False
    verbose_name_plural = "goals"


# Define a new User admin with the inline
class UserAdmin(BaseUserAdmin):
    inlines = [GoalsInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)