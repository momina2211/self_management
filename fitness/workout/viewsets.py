from decimal import Decimal

from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from djstripe.models import Customer
from djstripe.models import PaymentIntent
from fitness.workout.utils import create_stripe_products, update_stripe_products
from fitness.workout.models import Exercise, WorkoutPlan,ExerciseCategory
from fitness.workout.serializers import ExerciseSerializer, WorkoutPlanSerializer,ExerciseCategorySerializer,PurchaseWorkoutPlanSerializer
from purchase.models import Purchase
from users.pagination import CustomPageSizePagination

import stripe
import logging

logger = logging.getLogger(__name__)



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
        with transaction.atomic():
            workout_plan = serializer.save(user=user)

            if workout_plan.price and workout_plan.price >= Decimal('0.50'):
                try:
                    create_stripe_products(workout_plan, user)
                except stripe.error.StripeError as e:
                    logger.error(
                        f"Stripe Error for WorkoutPlan {workout_plan.id}: {str(e)}",
                        extra={
                            'user_id': user.id,
                            'workout_plan_id': workout_plan.id,
                            'price': float(workout_plan.price)
                        }
                    )

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user

        if instance.user != user:
            raise PermissionDenied("You are not authorized to update this workout plan.")

        with transaction.atomic():
            workout_plan = serializer.save()

            if 'price' in serializer.validated_data:
                try:
                    if workout_plan.stripe_product_id:
                        update_stripe_products(workout_plan)
                    elif workout_plan.price and workout_plan.price >= Decimal('0.50'):
                        create_stripe_products(workout_plan, user)
                except stripe.error.StripeError as e:
                    logger.error(
                        f"Stripe Update Error for WorkoutPlan {workout_plan.id}: {str(e)}",
                        extra={
                            'user_id': user.id,
                            'workout_plan_id': workout_plan.id,
                            'action': 'update'
                        }
                    )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def purchase(self, request):
        serializer = PurchaseWorkoutPlanSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        workout_plan = serializer.validated_data['workout_plan_id']
        payment_method_id = serializer.validated_data['payment_method_id']
        buyer = request.user

        try:
            if not buyer.stripe_customer:
                customer = Customer.create(subscriber=buyer)
                buyer.stripe_customer = customer
                buyer.save()

            # Create payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount= max(int(workout_plan.price * 100), 50),
                currency='usd',
                payment_method=payment_method_id,
                customer=buyer.stripe_customer.id,
                confirm=True,
                metadata={
                    'workout_plan_id': str(workout_plan.id),
                    'buyer_id': str(buyer.id),
                    'seller_id': str(workout_plan.user.id)
                },
                off_session=True,
                description=f"Purchase of workout plan: {workout_plan.name}"
            )
            PaymentIntent.sync_from_stripe_data(payment_intent)

            # If payment succeeded, create purchase record
            if payment_intent.status == 'succeeded':
                Purchase.objects.create(
                    buyer=buyer,
                    seller=workout_plan.user,
                    workout_plan=workout_plan,
                    amount=workout_plan.price,
                    stripe_payment_intent_id=payment_intent.id
                )
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
