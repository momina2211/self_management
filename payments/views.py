import stripe
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from djstripe.models import Customer,PaymentMethod

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_test_payment_method(request):
    """
    Creates a test payment method using Stripe tokens
    """
    try:
        customer, created = Customer.get_or_create(subscriber=request.user)
        if created:
            request.user.stripe_customer = customer
            request.user.save()

        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={"token": "tok_visa"},  # Using test token
        )

        # Attach to customer
        attached_pm = stripe.PaymentMethod.attach(
            payment_method.id,
            customer=customer.id,
        )

        # Sync with dj-stripe
        dj_payment_method = PaymentMethod.sync_from_stripe_data(attached_pm)

        return Response({
            "status": "success",
            "payment_method_id": dj_payment_method.id,
            "card_last4": dj_payment_method.card.last4,
            "customer_id": customer.id
        })

    except stripe.error.StripeError as e:
        return Response({
            "error": str(e),
            "type": "stripe_error"
        }, status=400)