
from django.urls import path
from . import views

app_name = 'frontend'  

urlpatterns = [
    path('', views.home_view, name='home'),
    path('personal/', views.personal_view, name='personal'),
    path('corperate/', views.corperate_view, name='corperate'),
    path('insurance/', views.insurance_view, name='insurance'),
    path('mortgages/', views.mortgages_view, name='mortgages'),
    path('savings/', views.savings_view, name='savings'),
    path('loans/', views.loans_view, name='loans'),
    path('cards/', views.cards_view, name='cards'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('terms/', views.terms_view, name='terms'),
]