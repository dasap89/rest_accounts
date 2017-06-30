"""The urls for the account-related actions in the api"""
from django.conf.urls import url

from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    UserInfoView,
    UpdateUserView,
)

# pylint: disable=invalid-name
app_name = 'api-auth'

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^info$', UserInfoView.as_view(), name='info'),
    url(r'^update$', UpdateUserView.as_view(), name='update'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
]
