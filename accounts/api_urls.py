# pylint: disable=missing-docstring
from django.conf.urls import url, include


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^auth/', include('main.api.urls', namespace='auth')),
]

