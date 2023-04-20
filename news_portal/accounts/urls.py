from django.urls import path, include

from news.views import upgrade_user
from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('', include('allauth.urls')),
    path('upgrade/', upgrade_user, name='account_upgrade'),
]