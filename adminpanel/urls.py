from django.urls import path
from . import views
urlpatterns = [
    path('',views.login),
    path('logout/',views.logout),
    path('register/',views.registeradmin),
    path('emailpasscheck/',views.emailpass_check),
    path('dashboard/',views.dashboard_admin),
    path('common/',views.product_common),
    path('color/',views.product_color),
    path('size/',views.product_size),
]
