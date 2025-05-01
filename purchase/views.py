from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from purchase.models import Purchase
from purchase.serializers import PurchaseSerializer
from users.pagination import CustomPageSizePagination


class PurchaseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return Purchase.objects.filter(buyer=self.request.user).order_by('-purchased_at')