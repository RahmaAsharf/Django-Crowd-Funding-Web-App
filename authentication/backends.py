from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # Check if the email and password are provided
        if email is None or password is None:
            return None
        
        # Find the user with the provided email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
        # Check if the user's account is activated
        if user.is_active:
            # Check the password
            if user.check_password(password):
                return user
        else:
            # Account is not activated
            return None
