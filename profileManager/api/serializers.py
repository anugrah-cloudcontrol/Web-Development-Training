# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Use PrimaryKeyRelatedField

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'location', 'birth_date']
class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Nested serializer for profile

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()