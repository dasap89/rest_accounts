"""Serializers for Accounts Application."""
from django.contrib.auth import get_user_model, password_validation
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    EmailField,
    CharField
)

# pylint: disable=invalid-name
User = get_user_model()


class LoginSerializer(Serializer):
    """Login serializer
    """
    email = EmailField(
        error_messages={
            'required': 'The email field should not be empty',
        }
    )
    password = CharField(
        error_messages={
            'required': 'The password field should not be empty',
        }
    )


class UserCreateSerializer(ModelSerializer):
    """Serializer for creating new users
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """Defines User model and fields that will be serialized."""
        model = User
        fields = (
            "email",
            "password"
        )
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        # CustomPasswordValidator.validate(password=password)

        user_obj = User(
            email=email,
        )

        user_obj.set_password(password)
        user_obj.save()

        # validated_data['token'] = Token.objects.create(user=user_obj)

        return validated_data


class UserInfoSerializer(ModelSerializer):
    """Serializer for User model"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Metaclass for User model serializer
        """
        model = User
        fields = ('email', 'is_staff', 'last_name', 'first_name')


class UserUpdateSerializer(ModelSerializer):
    """Serializer for Updating User model"""

    password = CharField(required=False, max_length=128)
    email = EmailField(required=False)

    # pylint: disable=too-few-public-methods
    class Meta:
        """Metaclass for User model serializer
        """
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', )

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value
