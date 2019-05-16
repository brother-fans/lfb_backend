from django.conf.urls import url

from .apis.auth_api import Login, Logout
from .apis.views import UserDetail

urlpatterns = [
    url(r'^login',
        Login.as_view(),
        name='login'),
    url(r'^logout',
        Logout.as_view(),
        name='logout'),
    url(r'^detail/user',
        UserDetail.as_view(),
        name='user_detail'),
]
