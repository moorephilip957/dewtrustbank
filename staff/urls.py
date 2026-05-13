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

    # functioons
    path(
        'toggle-sms-alert/<int:pk>/',
        toggle_sms_alert,
        name='toggle_sms_alert'
    ),
    path(
        'toggle-account-status/<int:pk>/',
        toggle_account_status,
        name='toggle_account_status'
    ),

    path(
        'staff/change-customer-password/<int:pk>/',
        change_customer_password,
        name='change_customer_password'
    ),

    path(
        'pending-transactions/',
        pending_transactions,
        name='pending_transactions'
    ),

    path(
        'approve-deposit/<int:pk>/',
        approve_deposit,
        name='approve_deposit'
    ),

    path(
        'decline-deposit/<int:pk>/',
        decline_deposit,
        name='decline_deposit'
    ),

    path(
        'approve-local-transfer/<int:pk>/',
        approve_local_transfer,
        name='approve_local_transfer'
    ),

    path(
        'decline-local-transfer/<int:pk>/',
        decline_local_transfer,
        name='decline_local_transfer'
    ),

    path(
        'approve-wire-transfer/<int:pk>/',
        approve_wire_transfer,
        name='approve_wire_transfer'
    ),

    path(
        'decline-wire-transfer/<int:pk>/',
        decline_wire_transfer,
        name='decline_wire_transfer'
    ),

    path(
        'view-deposit-proof/<int:pk>/',
        view_deposit_proof,
        name='view_deposit_proof'
    ),
]