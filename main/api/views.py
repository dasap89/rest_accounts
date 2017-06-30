"""Views for account application api"""
from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework import permissions


from .serializers import (
    UserCreateSerializer,
    LoginSerializer,
    UserInfoSerializer,
    UserUpdateSerializer,
)

from .utils import create_token


User = get_user_model()


class RegisterView(CreateAPIView):
    """
    View for registration new users
    
    Required:
        email and password
    Returned:
        - email in success
        - erros in fail
    """
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = User.objects.all()


class LoginView(APIView):
    """
    Log in user view
    
    Required:
        email and password
    Returned:
        - message and token in success
        - error in fail
    """
    authentication_classes = ()
    permission_classes = (permissions.AllowAny, )


    def post(self, request):
        """
        Post method that performs creation user session
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = auth.authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )

            if user is not None:
                token = create_token(user)
                message = 'user {} logged'\
                    .format(serializer.validated_data['email'])

                return Response({
                    'message': message,
                    'token': token
                })

            raise AuthenticationFailed(
                detail='Invalid credentials'
            )

        return Response(
            {'errors': serializer.errors},
            HTTP_400_BAD_REQUEST
        )


class UserInfoView(APIView):
    """
    Returns current user information
    
    Required:
        token in headers "Authorization: Token "+token
    """
    @staticmethod
    def get(request):
        """Request to get info of current user
        """
        serializer = UserInfoSerializer(request.user)

        return Response(serializer.data)


class UpdateUserView(UpdateAPIView):
    """
    View for updating personal info of user
    
    Required:
        token in headers "Authorization: Token "+token
    Optional:
        email, first_name, last_name, password
    Returned:
        - message in success
        - error in fail
    """
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        """PATCH or PUT method that will update personal data
        """
        # pylint: disable=attribute-defined-outside-init
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if serializer.data.get("email"):
                self.object.email = serializer.data.get("email")
            if serializer.data.get("first_name"):
                self.object.first_name = serializer.data.get("first_name")
            if serializer.data.get("last_name"):
                self.object.last_name = serializer.data.get("last_name")
            if serializer.data.get("password"):
                self.object.set_password(serializer.data.get("password"))
            self.object.save()
            return Response(
                {"detail": "Personal data is changed"},
                status=HTTP_200_OK
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Logout user that deletes token for user
    
    Required:
        token in headers "Authorization: Token "+token
    Returned:
        - message in success
        - error in fail
    """

    permission_classes = (permissions.IsAuthenticated,)

    # pylint: disable=no-self-use
    def delete(self, request):
        """DELETE method that removes token for 
        current user from database
        """
        request.user.auth_token.delete()
        message = 'user {} logged out'.format(request.user.email)
        return Response(
            {'message': message},
            HTTP_200_OK
        )