from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegistrationView, UserProfileViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # User profile endpoints
    path('', include(router.urls)),
]