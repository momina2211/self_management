from rest_framework import serializers

from fitness.workout.serializers import WorkoutPlanSerializer
from purchase.models import Purchase
from users.serializers import UserProfileSerializer


class PurchaseSerializer(serializers.ModelSerializer):
    workout_plan = WorkoutPlanSerializer()
    seller = UserProfileSerializer(source='seller.profile')

    class Meta:
        model = Purchase
        fields = ['id', 'workout_plan', 'seller', 'amount', 'purchased_at']