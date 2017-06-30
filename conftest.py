"""Additional configuration for pytest"""
import datetime
import os

import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()


# pylint: disable=redefined-outer-name,unused-argument,no-member
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Set up the database for tests that need it"""
    with django_db_blocker.unblock():
        user_one = User.objects.create_user(
            email='user_one@example.com',
            password='test_123'
        )

        Token.objects.create(user=user_one)


@pytest.mark.django_db
def get_token(email='user_one@example.com'):
    """
    Get user token from db
    :param user: User name
    :return: Key value from Token model object
    """
    test_user = User.objects.get(email=email)
    # pylint: disable=no-member
    return Token.objects.get(user_id=test_user.id).key
