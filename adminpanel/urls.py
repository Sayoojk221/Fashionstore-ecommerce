from django.urls import path
from . import views
urlpatterns = [
    path('',views.login),
    path('register/',views.registeradmin),
    path('emailpasscheck/',views.emailpass_check),
    path('dashboard/',views.dashboard_admin),
    path('common/',views.product_common),
]
