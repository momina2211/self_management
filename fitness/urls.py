from django.urls import path,include
from rest_framework.routers import DefaultRouter
from fitness.workout.viewsets import ExerciseViewSet, WorkoutPlanViewSet,ExerciseCategoryViewSet
from fitness.BMI.views import BMICalculateView


router=DefaultRouter()
#WORKOUT URLS
router.register(r'exercises', ExerciseViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet)
router.register(r'exercises_category', ExerciseCategoryViewSet)

urlpatterns = [

    #BMI URLS
    path('bmi/calculate/', BMICalculateView.as_view(), name='bmi-calculate'),
    path('',include(router.urls)),
]