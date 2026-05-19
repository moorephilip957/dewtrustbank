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
        'update-customer/<int:pk>/',
        update_customer,
        name='update_customer'
    ),

    path(
        'delete-customer/<int:pk>/',
        delete_customer,
        name='delete_customer'
    ),

    path(
        'fund-customer/',
        fund_customer,
        name='fund_customer'
    ),

    path(
        'debit-customer/',
        debit_customer,
        name='debit_customer'
    ),

    path(
        'kyc-requests/',
        kyc_requests,
        name='kyc_requests'
    ),

    path(
        'kyc-requests/<int:pk>/',
        kyc_detail,
        name='kyc_detail'
    ),

    path('kyc-approve/<int:pk>/', approve_kyc, name='approve_kyc'),
    path('kyc-reject/<int:pk>/', reject_kyc, name='reject_kyc'),

    path(
        'tickets/',
        ticket_list,
        name='ticket_list'
    ),
    path(
        'tickets/<int:pk>/',
        ticket_detail,
        name='ticket_detail'
    ),

    path(
        'card-applications/',
        card_applications,
        name='card_applications'
    ),

    path(
        'card-application/<int:pk>/approve/',
        approve_card_application,
        name='approve_card_application'
    ),

    path(
        'card-application/<int:pk>/decline/',
        decline_card_application,
        name='decline_card_application'
    ),

    path(
        'deactivate-card/<int:pk>/',
        deactivate_card,
        name='deactivate_card'
    ),

    path(
        'activate-card/<int:pk>/',
        activate_card,
        name='activate_card'
    ),

    path(
        'loan-applications/',
        loan_applications,
        name='loan_applications'
    ),

    path(
        'loan/<int:pk>/process/',
        process_loan,
        name='process_loan'
    ),

    path(
        'loan/<int:pk>/approve/',
        approve_loan,
        name='approve_loan'
    ),

    path(
        'loan/<int:pk>/reject/',
        reject_loan,
        name='reject_loan'
    ),

    path(
        'customer-details/<int:pk>/',
        customer_details,
        name='customer_details'
    ),

    path(
        'history/edit/<int:pk>/',
        edit_history,
        name='edit_history'
    ),

    path(
        'history/delete/<int:pk>/',
        delete_history,
        name='delete_history'
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

    path(
        'copy-transaction-history/',
        copy_transaction_history,
        name='copy_transaction_history'
    ),
]