from django.utils import timezone
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Category, Tag
from .serializers import TaskSerializer, CategorySerializer, TagSerializer
from users.pagination import CustomPageSizePagination


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageSizePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact', 'in'],
        'priority': ['exact', 'in'],
        'completed': ['exact'],
        'due_date': ['exact', 'lt', 'gt', 'lte', 'gte'],
        'category__name': ['exact', 'icontains'],
        'tags__name': ['exact', 'icontains'],
    }
    search_fields = ['title', 'description']
    ordering_fields = ['Created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-Created_at']

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)

        # Filter by completion status
        completed = self.request.query_params.get('completed', None)
        if completed == 'true':
            queryset = queryset.filter(completed=True)
        elif completed == 'false':
            queryset = queryset.filter(completed=False)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.save()
        return Response({'status': 'task marked as complete'})

    @action(detail=True, methods=['post'])
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        task.completed = False
        task.save()
        return Response({'status': 'task marked as incomplete'})

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        queryset = self.get_queryset().filter(
            due_date__gte=timezone.now().date(),
            completed=False
        ).order_by('due_date')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)