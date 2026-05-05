
from django.urls import path
from . import views

app_name = 'frontend'  # this is the namespace

urlpatterns = [
    path('', views.home_view, name='home'),
    path('personal/', views.personal_view, name='personal'),
    path('corperate/', views.corperate_view, name='corperate'),
    path('insurance/', views.insurance_view, name='insurance'),
]