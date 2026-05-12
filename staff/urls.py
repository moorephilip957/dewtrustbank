from django.urls import path
from .views import *

app_name = 'staff'
urlpatterns = [
    path('dashboard/', staff_dashboard, name='staff_dashboard'),
    path(
        'account-holders/',
        account_holders,
        name='account_holders'
    ),

    path(
        'fund-account/',
        fund_account,
        name='fund_account'
    ),

    path(
        'debit-account/',
        debit_account,
        name='debit_account'
    ),

    path(
        'kyc-management/',
        kyc_management,
        name='kyc_management'
    ),

    path(
        'customer-details/<int:pk>/',
        customer_details,
        name='customer_details'
    ),
]