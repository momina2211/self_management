from django.urls import path
from .views import SignUpView,LoginView,RequestPasswordResetView,PasswordResetConfirmView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('auth/password-reset/', RequestPasswordResetView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]