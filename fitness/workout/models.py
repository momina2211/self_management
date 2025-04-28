from users.models import User
from users.utils.models import UUIDMODEL
from django.db import models


class ExerciseCategory(UUIDMODEL):
    name = models.CharField(max_length=100)
    Exercises = models.ManyToManyField('Exercise', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Exercise(UUIDMODEL):
    name = models.CharField(max_length=100)
    instructions = models.TextField(null=True, blank=True)
    default_reps = models.IntegerField(null=True, blank=True)
    default_sets = models.IntegerField(null=True, blank=True)
    rest_time_seconds = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class WorkoutPlan(UUIDMODEL):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('custom', 'Custom')
    ]
    class VisibilityChoices(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Private'

    exercise = models.ManyToManyField(Exercise,blank=True)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    visibility = models.CharField(max_length=20, choices=VisibilityChoices.choices, default=VisibilityChoices.PUBLIC)
    def __str__(self):
        return self.name



