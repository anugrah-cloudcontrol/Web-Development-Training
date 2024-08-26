from rest_framework import generics
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, UserWithProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from .authentication import CustomAccessToken

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserWithProfileSerializer

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            profile_data = {
                'user': user.id,  # Provide only the user ID here
                'bio': request.data.get('bio', ''),
                'location': request.data.get('location', ''),
                'birth_date': request.data.get('birth_date', None)
            }
            profile_serializer = ProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                user.set_password(request.data.get('password'))  # Hash the password
                user.save()  # Save the user with the hashed password
                profile_serializer.save()  # Save the profile

                return Response({
                    "user": user_serializer.data,
                    "profile": profile_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                user.delete()  # Rollback user creation if profile fails
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserWithProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Update user details
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        
        if user_serializer.is_valid():
            user = user_serializer.save()

            # Check if profile exists, if not, create one
            profile, created = Profile.objects.get_or_create(user=user)
            profile_data = request.data.get('profile')
            # print("Profile data :: ",profile_data)
            
            profile_serializer = ProfileSerializer(profile, data=profile_data, partial=True)
            
            if profile_serializer.is_valid():
                # print(profile_serializer.validated_data)
                profile_serializer.save()

                return Response({
                    "user": user_serializer.data,
                    "profile": profile_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializers import LoginSerializer
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access = CustomAccessToken.for_user(user) 
            return Response({
                'refresh': str(refresh),
                'access': str(access),
                # Optionally include additional user data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def post(self, request, *args, **kwargs):
        try:
            # This will blacklist the user's current refresh token
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()  # If using `django-rest-framework-simplejwt` with blacklist support
            
            # Optionally, you can also logout the user from the Django session
            logout(request)
            
            return Response({'detail': 'Successfully logged out from all sessions.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
