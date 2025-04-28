from django.contrib import admin
from fitness.workout.models import Exercise,ExerciseCategory,WorkoutPlan
admin.site.register(ExerciseCategory)
admin.site.register(Exercise)
admin.site.register(WorkoutPlan)


