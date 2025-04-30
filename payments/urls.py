from django.urls import path

from .views import create_test_payment_method

urlpatterns = [
    # ...
    path('create-test-payment-method/', create_test_payment_method),
]