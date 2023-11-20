"""
Models for the Workout Designer app.
"""
from django.contrib.auth.models import User
from django.db import models

from workout_log.models import Exercise


class Routine(models.Model):
    """A routine created by the Workout Designer"""
    SPLIT_CHOICES = [
        ("Arnold", "Arnold"),
        ("Bro", "Bro"),
        ("PPL", "Push-Pull-Legs"),
        ("UL", "Upper-Lower"),
    ]

    name = models.CharField(max_length=40)
    date_created = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    split = models.CharField(max_length=6, choices=SPLIT_CHOICES)
    is_synchronous = models.BooleanField()
    lower_limit_min = models.FloatField()
    upper_limit_min = models.FloatField()
    is_muscle_focused = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.name} | {self.split}"


class Day(models.Model):
    """A day in a routine. Ex: Push day, Back-Chest day, Lower day."""
    TYPES_OF_DAYS = [
        ("Push", "Push"),
        ("Pull", "Pull"),
        ("Legs", "Legs"),
        ("Upper", "Upper"),
        ("Lower", "Lower"),
        ("Chest", "Chest"),
        ("Back", "Back"),
        ("Shoulders", "Shoulders"),
        ("Arms", "Arms"),
        ("BC", "Back-Chest"),
        ("SA", "Shoulders-Arms"),
    ]

    name = models.CharField(max_length=20)  # usually the same as focus, but there might be variation
    focus = models.CharField(max_length=10, choices=TYPES_OF_DAYS)
    time_est_min = models.FloatField()
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} | {self.time_est_min} | {self.routine}"


class PlannedSets(models.Model):
    """Planned sets for a day. Ex: Bench press, 3x6."""
    exercise = models.ForeignKey(Exercise, on_delete=models.RESTRICT)
    num_sets = models.IntegerField()
    reps = models.IntegerField()
    time_est_min = models.FloatField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'planned sets'

    def __str__(self) -> str:
        return f"{self.exercise}, {self.num_sets}x{self.reps}"

