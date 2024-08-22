# urls.py
from django.urls import path
from .views import UserCreateAPIView, UserListAPIView, UserProfileAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('api/register/', UserCreateAPIView.as_view(), name='api-register'),
    path('api/users/', UserListAPIView.as_view(), name='api-users'),  # New endpoint for listing users and profiles
    path('api/profile/<int:id>/', UserProfileAPIView.as_view(), name='api-user-profile'),  # New endpoint for a single user's profile
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),



]
