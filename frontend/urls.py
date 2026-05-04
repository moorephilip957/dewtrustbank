
from django.urls import path
from . import views

app_name = 'frontend'  # this is the namespace

urlpatterns = [
    path('', views.home_view, name='home'),
    # path('about/', views.about, name='about'),
]