from fitness.workout.models import WorkoutPlan
from users.models import User
from users.utils.models import UUIDMODEL
from django.db import models


class Purchase(UUIDMODEL):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent_id = models.CharField(max_length=100)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'workout_plan')