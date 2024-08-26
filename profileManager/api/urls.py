from django.urls import path
from .views import UserCreateAPIView, UserListAPIView, UserProfileAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('api/register/', UserCreateAPIView.as_view(), name='api-register'),
    path('api/users/', UserListAPIView.as_view(), name='api-users'),
    path('api/profile/', UserProfileAPIView.as_view(), name='api-user-profile'),
    path('api/profile/update/', UserProfileAPIView.as_view(), name='api-user-update'),  # New endpoint for user update
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),
]
