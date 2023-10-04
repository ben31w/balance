"""
Models for the Workout Log:
- Exercise
- Muscle
- MuscleWorked
- Set
"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Exercise(models.Model):
    """
    An exercise that the user can log.
    Fields:
    - name
    - isCompound
    - equipment
    - createdBy
    Exercises can have the same name but different equipments, making
    them different exercises. There is a constraint to check this rule.
    Ex: bench press (barbell), bench press (dumbbells)
    """
    name = models.CharField(max_length=40)
    isCompound = models.BooleanField()
    BARBELL = "BB"
    DUMBBELLS = "DB"
    CABLES = "CB"
    MACHINE = "MC"
    HEXBAR = "HB"
    KETTLEBELL = "KB"
    RESISTANCE_BAND = "RB"
    BODYWEIGHT = "BW"
    EQUIPMENT_CHOICES = [
        (BARBELL, "Barbell"),
        (DUMBBELLS, "Dumbbells"),
        (CABLES, "Cables"),
        (MACHINE, "Machine"),
        (HEXBAR, "Hexbar"),
        (KETTLEBELL, "Kettlebell"),
        (RESISTANCE_BAND, "Resistance Band"),
        (BODYWEIGHT, "Bodyweight"),
    ]
    equipment = models.CharField(max_length=2, choices=EQUIPMENT_CHOICES)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # Check that this exercise doesn't already exist before saving it.
    #  Unfortunately this interferes with trying to edit an exercise.
    #  Can this be done through Django constraints instead?
    def clean(self):
        for exercise in Exercise.objects.all():
            if self.__str__().lower() == exercise.__str__().lower():
                raise ValidationError('An exercise with identical name and '
                                      'equipment already exists.')

    def __str__(self):
        return f"{self.name} ({self.equipment})"


class Muscle(models.Model):
    """
    A muscle that an exercise works.
    """
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class MuscleWorked(models.Model):
    """
    A muscle worked by an exercise. Stores whether the exercise directly
    targets a muscle, or if it's secondary.
    ex: Bench press, Chest, True. Bench press, Triceps, False.
    """
    exercise = models.ForeignKey(Exercise, on_delete=models.RESTRICT)
    muscle = models.ForeignKey(Muscle, on_delete=models.RESTRICT)
    directlyTargets = models.BooleanField()

    class Meta:
        verbose_name_plural = 'muscles worked'

    def __str__(self):
        if self.directlyTargets:
            return f"{self.exercise}, {self.muscle}, Direct"
        return f"{self.exercise}, {self.muscle}, Indirect"


class Set(models.Model):
    """
    A set logged by a user.
    Each set tracks a date, number of reps, weight, exercise, and the user who
    logged it.
    """
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, on_delete=models.RESTRICT)
    reps = models.IntegerField()
    weight = models.FloatField()
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}, {self.logged_by}, {self.date}, {self.exercise}, {self.reps} reps at {self.weight} lbs."

