from django.urls import path
from .models import *
from customer import views

urlpatterns = [
    path('',views.home),
]
