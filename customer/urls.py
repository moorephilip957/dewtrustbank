from django.urls import path
from . import views

app_name = 'customer'  

urlpatterns = [
        path('dashboard/', views.dashboard, name='dashboard'), 
]