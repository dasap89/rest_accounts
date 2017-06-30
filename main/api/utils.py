from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

def create_token(user):	
    token, _ = Token.objects.get_or_create(user=user)
    return token.key

def get_token(email='user_one@example.com'):
    test_user = User.objects.get(email=email)
    return Token.objects.get(user_id=test_user.id).key