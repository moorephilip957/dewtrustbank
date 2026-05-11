from django.urls import path
from .views import kyc_verification, kyc_terms

app_name = 'kyc'
urlpatterns = [
    path('terms-condition/', kyc_terms, name='kyc_terms'),
    path('verification/', kyc_verification, name='kyc_verification'),
]