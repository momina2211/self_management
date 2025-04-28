from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from fitness.workout.models import Exercise, WorkoutPlan,ExerciseCategory
from fitness.workout.serializers import ExerciseSerializer, WorkoutPlanSerializer,ExerciseCategorySerializer
from users.pagination import CustomPageSizePagination


class ExerciseCategoryViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPageSizePagination
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer
    permission_classes = [IsAuthenticated]

class ExerciseViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPageSizePagination
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all().prefetch_related('exercise')
    serializer_class = WorkoutPlanSerializer
    pagination_class = CustomPageSizePagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return WorkoutPlan.objects.filter(Q(user=user) | Q(visibility=WorkoutPlan.VisibilityChoices.PUBLIC))
        else:
            return WorkoutPlan.objects.filter(visibility=WorkoutPlan.VisibilityChoices.PUBLIC)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
