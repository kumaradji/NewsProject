from django.urls import path, include

from news.views import upgrade_user
from .views import SignUp

urlpatterns = [
    path('', include('allauth.urls')),
    path('upgrade/', upgrade_user, name='account_upgrade'),
]