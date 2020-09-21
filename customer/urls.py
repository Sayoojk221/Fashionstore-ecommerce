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
    path('productsingle/',views.product_single),
    path('productsingleuseraccount/',views.product_single_useraccount),
    path('customersmacid/',views.customersmacid),
    path('addtocart/',views.addtocart),
    path('sidecart/',views.sidecart),
]
