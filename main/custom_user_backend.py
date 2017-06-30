from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


UserModel = get_user_model()


class CustomBackend(ModelBackend):

    def authenticate(self, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.filter(
                email__iexact=email
            ).distinct()
        except UserModel.DoesNotExist:
            return None

        if user.exists():
            user_obj = user.first()
            if user_obj.check_password(password):
                return user_obj
            return  None
        else:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
           return None
