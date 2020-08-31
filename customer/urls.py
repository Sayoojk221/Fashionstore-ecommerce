from django.urls import path
from .models import *
from customer import views

urlpatterns = [
    path('',views.home),
    path('account/',views.account_user),
    path('register/',views.user_register),
    path('emailpasswordcheck/',views.emailpassword),
    path('emailpasswordchecklogin/',views.emailpasswordlogin),
    path('login/',views.user_login),
]
