"""
Models for the Workout Log:
- Exercise
- Muscle
- MuscleWorked
- Set
"""
from django.contrib.auth.models import User
from django.db import models


class Exercise(models.Model):
    """
    An exercise that the user can log.
    Fields:
    - name
    - isCompound
    - equipment
    Exercises can have the same name but different equipments, making
    them different exercises.
    Ex: bench press (barbell), bench press (dumbbells)
    """
    name = models.CharField(max_length=40)
    isCompound = models.BooleanField()
    BARBELL = "BB"
    DUMBBELLS = "DB"
    CABLES = "CB"
    MACHINE = "MC"
    BODYWEIGHT = "BW"
    EQUIPMENT_CHOICES = [
        (BARBELL, "Barbell"),
        (DUMBBELLS, "Dumbbells"),
        (CABLES, "Cables"),
        (MACHINE, "Machine"),
        (BODYWEIGHT, "Bodyweight")
    ]
    equipment = models.CharField(max_length=2, choices=EQUIPMENT_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.equipment})"


class Muscle(models.Model):
    """
    A muscle that an exercise works.
    """
    name = models.CharField(max_length=25)


class MuscleWorked(models.Model):
    """
    A muscle worked by an exercise. Stores whether the exercise directly
    targets a muscle, or if it's secondary.
    ex: Bench press, Chest, True. Bench press, Triceps, False.
    """
    exercise = models.ForeignKey(Exercise, on_delete=models.RESTRICT)
    muscle = models.ForeignKey(Muscle, on_delete=models.RESTRICT)
    directlyTargets = models.BooleanField()


class Set(models.Model):
    """
    A set logged by a user.
    Each set tracks a date, number of reps, weight, exercise, and the user who
    logged it.
    """
    date = models.DateField()
    reps = models.IntegerField()
    weight = models.FloatField()
    exercise = models.ForeignKey(Exercise, on_delete=models.RESTRICT)
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE)

