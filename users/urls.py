from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import SignUpView,LoginView,RequestPasswordResetView,PasswordResetConfirmView
from .viewsets import ProfileViewSet

router=DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('auth/password-reset/', RequestPasswordResetView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('', include(router.urls)),
]

