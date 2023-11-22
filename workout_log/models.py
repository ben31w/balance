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
    - is_compound
    - equipment
    - created_by
    Exercises can have the same name but different equipments, making
    them different exercises. There is a constraint to check this rule.
    Ex: bench press (barbell), bench press (dumbbells)
    """
    name = models.CharField(max_length=40)
    is_compound = models.BooleanField()
    BARBELL = "BB"
    DUMBBELLS = "DB"
    CABLES = "C"
    MACHINE = "M"
    SMITH_MACHINE = "SM"
    HEXBAR = "HB"
    KETTLEBELL = "KB"
    RESISTANCE_BAND = "RB"
    BODYWEIGHT = "BW"
    EQUIPMENT_CHOICES = [
        (BARBELL, "Barbell"),
        (DUMBBELLS, "Dumbbells"),
        (CABLES, "Cables"),
        (MACHINE, "Machine"),
        (SMITH_MACHINE, "Smith Machine"),
        (HEXBAR, "Hexbar"),
        (KETTLEBELL, "Kettlebell"),
        (RESISTANCE_BAND, "Resistance Band"),
        (BODYWEIGHT, "Bodyweight"),
    ]
    equipment = models.CharField(max_length=2, choices=EQUIPMENT_CHOICES)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ["name", "equipment"]

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
    directly_targets = models.BooleanField()

    class Meta:
        verbose_name_plural = 'muscles worked'

    def __str__(self):
        if self.directly_targets:
            return f"{self.exercise}, {self.muscle}, Direct"
        return f"{self.exercise}, {self.muscle}, Indirect"


class Set(models.Model):
    """
    A set logged by a user.
    Info entered by user:
    - date
    - exercise
    - reps
    - weight
    Info tracked internally:
    - user who logged the set
    - index (order) of the set, in relation to other sets on the same day
      (sets can then be moved around by the user)
    """
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, on_delete=models.RESTRICT)
    reps = models.IntegerField()
    weight = models.FloatField()
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE)
    index = models.IntegerField()

    def __str__(self):
        return f"{self.id}, {self.logged_by}, {self.date}, {self.exercise}, {self.reps} reps at {self.weight} lbs."

