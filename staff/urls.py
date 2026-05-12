from django.urls import path
from .views import *

app_name = 'staff'
urlpatterns = [
    path('dashboard/', staff_dashboard, name='staff_dashboard'),
]