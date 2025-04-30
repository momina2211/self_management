from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from purchase.models import Purchase
from purchase.serializers import PurchaseSerializer


class PurchaseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(buyer=self.request.user)