from django.urls import path
from . import views

app_name = 'account'  

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('otp/', views.pin_verify_view, name='verify_pin'),
    path(
        'resend-otp/',
        views.resend_login_otp,
        name='resend_login_otp'
    ),
    path('logout/', views.logout_view, name='logout'),

]