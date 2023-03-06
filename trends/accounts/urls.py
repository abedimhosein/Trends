from django.urls import path
from .apis import RegisterApi, ProfileApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('profile/', ProfileApi.as_view(), name='profile'),
    path('jwt/login/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
