from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


# Taken from
# http://www.djangorocks.com/tutorials/creating-a-custom-authentication-backend/creating-a-simple-authentication-backend.html
# Backend for login with email
class EmailAuth:
    @staticmethod
    def authenticate(username="", password="", **kwargs):
        try:
            user = User.objects.get(email__iexact=username)
            if check_password(password, user.password):
                return user
            else:
                return None
        except User.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class PhoneAuth:
    @staticmethod
    def authenticate(username="", password="", **kwargs):
        try:
            user = User.objects.get(profile__phone=username)
            if check_password(password, user.password):
                return user
            else:
                return None
        except User.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
