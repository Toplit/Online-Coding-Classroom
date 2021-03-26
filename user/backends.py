from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CaseInsensitiveModelBackend(ModelBackend):
    """ Class for ensuring login email is case insensitive """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Get the custom user model
        UserModel = get_user_model()
        # Set the username if it is None
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)        
        try:
            # Change the username to be case insensitive
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            # Get the user using their username
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            # If the user does not exist, set the password as None for now
            UserModel().set_password(password)
        else:
            # If the password is correct, return the case insensitve user
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
