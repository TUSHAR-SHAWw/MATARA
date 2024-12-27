# backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile  # Import the UserProfile model

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the username is an email or phone number
            if '@' in username:
                # If it's an email, look up by email
                user = User.objects.get(email=username)
            else:
                # Otherwise, treat it as a phone number
                # Access the profile using the OneToOne relationship
                user_profile = UserProfile.objects.get(phone=username)
                user = user_profile.user  # Access the related User

            # Check the user's password
            if user.check_password(password):
                return user
        except (User.DoesNotExist, ObjectDoesNotExist):
            return None
