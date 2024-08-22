from rest_framework_simplejwt.tokens import AccessToken

class CustomAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        # Add additional information to the payload
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser  # Add superuser flag
        token['user_id'] = user.id
        return token
