from django.contrib.auth.backends import BaseBackend
from user_personalization.models import User


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get()
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get()
        except User.DoesNotExist:
            return None
