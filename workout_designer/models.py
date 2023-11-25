"""
Models for the Workout Designer app.
"""
from django.contrib.auth.models import User
from django.db import models

from workout_log.models import Exercise, Muscle


class Routine(models.Model):
    """A routine created by the Workout Designer"""
    ARN = "ARN"
    BRO = "BRO"
    PPL = "PPL"
    UL = "UL"
    SPLIT_CHOICES = [
        (ARN, "Arnold"),
        (BRO, "Bro"),
        (PPL, "Push-Pull-Legs"),
        (UL, "Upper-Lower"),
    ]

    datetime_created = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    split = models.CharField(max_length=3, choices=SPLIT_CHOICES)
    is_synchronous = models.BooleanField()
    lower_limit_min = models.FloatField()
    upper_limit_min = models.FloatField()
    is_muscle_focused = models.BooleanField()

    def __str__(self) -> str:
        name = ""
        match self.split:
            case Routine.ARN:
                name += "Arnold"
            case Routine.BRO:
                name += "Bro"
            case Routine.PPL:
                name += "Push-Pull-Legs"
            case Routine.UL:
                name += "Upper-Lower"
        match self.is_synchronous:
            case True:
                name += ", Synchronous"
            case False:
                name += ", Asynchronous" 
        return name


class DayType(models.Model):
    """A type of day"""
    PUSH = "PUSH"
    PULL = "PULL"
    LEGS = "LEGS"
    UPPER = "UPPER"
    LOWER = "LOWER"
    CHEST = "CHEST"
    BACK = "BACK"
    SHOULDERS = "SHOULDERS"
    ARMS = "ARMS"
    BC = "BC"
    SA = "SA"
    REST = "REST"
    TYPES_OF_DAYS = [
        (PUSH, "Push"),
        (PULL, "Pull"),
        (LEGS, "Legs"),
        (UPPER, "Upper"),
        (LOWER, "Lower"),
        (CHEST, "Chest"),
        (BACK, "Back"),
        (SHOULDERS, "Shoulders"),
        (ARMS, "Arms"),
        (BC, "Back-Chest"),
        (SA, "Shoulders-Arms"),
        (REST, "Rest"),
    ]

    name = models.CharField(max_length=10, choices=TYPES_OF_DAYS)

    def __str__(self) -> str:
        return self.name


class Focus(models.Model):
    """
    Defines a relationship between a day type and the muscles it focuses on.
    ex: PUSH focuses on chest, triceps, front delts, and lateral delts.
    """
    day_type = models.ForeignKey(DayType, on_delete=models.RESTRICT)
    muscle = models.ForeignKey(Muscle, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = 'focii'

    def __str__(self) -> str:
        return f"{self.day_type}: {self.muscle}"


class Day(models.Model):
    """A day in a routine, with a type, time estimate, and list of sets"""
    name = models.CharField(max_length=20)
    time_est_min = models.FloatField()
    day_type = models.ForeignKey(DayType, on_delete=models.RESTRICT, null=True)  # temporarily allow null
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} ({self.time_est_min} min.)"


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

