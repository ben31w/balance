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

    def __str__(self) -> str:
        if (self.user is None or self.user == "") and (self.producer is None or self.producer == ""):
            return f"{self.name}"
        elif self.user is None or self.user == "":
            return f"{self.name}, {self.producer}"
        elif self.producer is None or self.producer == "":
            return f"{self.name} , {self.user}"
        return f"{self.name}, {self.producer} , {self.user}"


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

    def __str__(self) -> str:
        return f"{self.name} of {self.food_item}"
    

class Contains(models.Model):
    """Link between a recipe and a food item the recipe contains"""
    # TODO figure how to handle what happens to this class if the 
    #  food item or unit it is linked to is deleted
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.RESTRICT)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'contains'


class LoggedFoodItem(models.Model):
    """An instance of a food item logged by a user"""
    date = models.DateField()
    food_item = models.ForeignKey(FoodItem, on_delete=models.RESTRICT)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.RESTRICT)
    meal = models.IntegerField()  # 0 for snack, 1 for breakfast, 2 for lunch, etc.
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.food_item.name} | {self.quantity}x{self.unit.name}"


class Goals(models.Model):
    """
    The fitness goals of a user. This class is not a standalone model. It is a 
    collection of additional fields to track about a user ('profile model').
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_calories = models.IntegerField()
