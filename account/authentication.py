from django.contrib.auth.models import User


class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):
        """
        Authenticate a user.

        Parameters:
        - request: The current request.
        - username: The email address used for authentication.
        - password: The user's password.

        Returns:
        - user: The authenticated user if successful, or None otherwise.
        """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None