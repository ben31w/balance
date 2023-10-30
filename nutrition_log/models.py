from django.contrib.auth.models import User
from django.db import models


class DailyWeight(models.Model):
    """A weight that a user can log for the day"""
    # TODO maybe validate that weight > 0
    date = models.DateField()
    weight = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # User + date combo needs to be unique, so the user can't log 
    #  multiple weights for one day.
    class Meta:
        unique_together = ["user", "date"]

    def __str__(self):
        return f"{self.user.username} | {self.date} | {self.weight}"


class FoodItem(models.Model):
    """A food item that a user can log"""
    # Should users be allowed to delete food items?
    name = models.CharField(max_length=100)
    producer = models.CharField(blank=True, max_length=25)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class Recipe(models.Model):
    """A collection of food items that a user can log"""
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class Unit(models.Model):
    """A unit that a food item can be measured in"""
    # Should users be allowed to delete units?
    name = models.CharField(max_length=25)
    calsPerUnit = models.FloatField()
    proPerUnit = models.FloatField()
    carbsPerUnit = models.FloatField()
    fatsPerUnit = models.FloatField()
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    

class Contains(models.Model):
    """Link between a recipe and a food item the recipe contains"""
    # TODO figure how to handle what happens to this class if the 
    #  food item or unit it is linked to is deleted
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.RESTRICT)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class LoggedFoodItem(models.Model):
    """An instance of a food item logged by a user"""
    date = models.DateField()
    food_item = models.ForeignKey(FoodItem, on_delete=models.RESTRICT)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.RESTRICT)
    meal = models.IntegerField()  # 0 for snack, 1 for breakfast, 2 for lunch, etc.
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
