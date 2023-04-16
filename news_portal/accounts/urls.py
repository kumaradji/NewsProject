from allauth.account.views import LogoutView
from django.urls import path
from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]