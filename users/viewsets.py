from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from users.pagination import CustomPageSizePagination
from users.models import UserProfile
from users.serializers import UserProfileSerializer


class ProfileViewSet(UpdateModelMixin,ListModelMixin,viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    pagination_class = CustomPageSizePagination
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


