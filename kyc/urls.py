from django.urls import path
from .views import kyc_verification

urlpatterns = [
    path(
        'kyc-verification/',
        kyc_verification,
        name='kyc_verification'
    ),
]