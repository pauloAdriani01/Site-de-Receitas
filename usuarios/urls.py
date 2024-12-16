from django.urls import path
from .views import LoginPageView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('loginPage/', LoginPageView.as_view(), name='loginPage'),
    path('logout/', LogoutView.as_view(), name='logout')
]