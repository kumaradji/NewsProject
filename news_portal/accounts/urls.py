from allauth.account.views import LogoutView
from django.urls import path
from .views import SignUp, Logout

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', Logout.as_view(), name='logout'),
]