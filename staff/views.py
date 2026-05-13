from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from transaction.models import (
    Deposit,
    LocalTransfer,
    InternationalTransfer,
    TransactionHistory,
)
from transaction.utils import generate_reference
from account.models import CustomUser
from .decorators import staff_required
from customer.models import UserBankAccount
from notification.utils import create_notification


@login_required
@staff_required
def staff_dashboard(request):
    return render(request, 'staff/dashboard.html')


@login_required
@staff_required
def account_holders(request):

    customers = UserBankAccount.objects.select_related(
        'user'
    ).all().order_by('-id')

    context = {
        'customers': customers
    }

    return render(
        request,
        'staff/account_holders.html',
        context
    )

@login_required
@staff_required
def fund_account(request):
    return render(request, 'staff/fund_account.html')

@login_required
@staff_required
def debit_account(request):
    return render(request, 'staff/debit_account.html')

@login_required
@staff_required
def kyc_management(request):
    return render(request, 'staff/kyc_management.html')


@login_required
@staff_required
def customer_details(request, pk):

    customer = get_object_or_404(
        UserBankAccount.objects.select_related('user'),
        pk=pk
    )

    # Deposits
    deposits = Deposit.objects.filter(
        user=customer.user
    ).order_by('-created_at')

    # Local Transfers
    local_transfers = LocalTransfer.objects.filter(
        user=customer.user
    ).order_by('-created_at')

    # International Transfers
    wire_transfers = InternationalTransfer.objects.filter(
        user=customer.user
    ).order_by('-created_at')

    context = {
        'customer': customer,
        'deposits': deposits,
        'local_transfers': local_transfers,
        'wire_transfers': wire_transfers,
    }

    return render(
        request,
        'staff/customer_details.html',
        context
    )


@login_required
@staff_required
def pending_transactions(request):

    deposits = Deposit.objects.filter(
        status='pending'
    ).select_related('user').order_by('-created_at')

    local_transfers = LocalTransfer.objects.filter(
        status='pending'
    ).select_related('user').order_by('-created_at')

    wire_transfers = InternationalTransfer.objects.filter(
        status='pending'
    ).select_related('user').order_by('-created_at')

    context = {
        'deposits': deposits,
        'local_transfers': local_transfers,
        'wire_transfers': wire_transfers,
    }

    return render(
        request,
        'staff/pending_transactions.html',
        context
    )


@login_required
@staff_required
def toggle_sms_alert(request, pk):

    user = get_object_or_404(
        CustomUser,
        pk=pk
    )

    # Toggle SMS Alert
    if user.sms_alert == 'activate':
        user.sms_alert = 'deactivate'
        messages.success(
            request,
            'SMS alert deactivated successfully.'
        )

    else:
        user.sms_alert = 'activate'
        messages.success(
            request,
            'SMS alert activated successfully.'
        )

    user.save()

    return redirect(
        'staff:customer_details',
        pk=user.bank_account.pk
    )


@login_required
@staff_required
def toggle_account_status(request, pk):

    user = get_object_or_404(
        CustomUser,
        pk=pk
    )

    # Toggle Status
    if user.status == 'active':

        user.status = 'blocked'

        messages.warning(
            request,
            'Customer account has been blocked.'
        )

    else:

        user.status = 'active'

        messages.success(
            request,
            'Customer account has been activated.'
        )

    user.save()

    return redirect(
        'staff:customer_details',
        pk=user.bank_account.pk
    )


@login_required
@staff_required
def change_customer_password(request, pk):

    user = get_object_or_404(
        CustomUser,
        pk=pk
    )

    if request.method == 'POST':

        password = request.POST.get('password')
        confirm_password = request.POST.get(
            'confirm_password'
        )

        # Validate
        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect(
                'staff:customer_details',
                pk=user.bank_account.pk
            )

        # Set Password
        user.set_password(password)

        user.save()

        messages.success(
            request,
            'Customer password changed successfully.'
        )

        return redirect(
            'staff:customer_details',
            pk=user.bank_account.pk
        )

    return redirect(
        'staff:customer_details',
        pk=user.bank_account.pk
    )


# transaxction approvals and rejection
@login_required
@staff_required
@transaction.atomic
def approve_deposit(request, pk):

    deposit = get_object_or_404(
        Deposit,
        pk=pk,
        status='pending'
    )

    bank_account = deposit.user.bank_account

    # Add Balance
    bank_account.balance += deposit.amount
    bank_account.save()

    # Update Deposit Status
    deposit.status = 'confirmed'
    deposit.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=deposit.user,
        amount=deposit.amount,
        transaction_type='deposit',
        direction='credit',
        description=f"Approved {deposit.method} deposit",
        reference=generate_reference(),
        status="successful",

        beneficiary_name="****self",
        beneficiary_number="******self",
        bank_name="Dew Trust Bank",
    )

    # Notification
    create_notification(
        user=deposit.user,
        title="Deposit Approved",
        message=f"Your deposit of {bank_account.get_currency_symbol()}{deposit.amount} has been approved successfully.",
        notif_type="success",
        related_object=deposit
    )

    messages.success(
        request,
        'Deposit approved successfully.'
    )

    return redirect('staff:pending_transactions')


@login_required
@staff_required
@transaction.atomic
def decline_deposit(request, pk):

    deposit = get_object_or_404(
        Deposit,
        pk=pk,
        status='pending'
    )

    deposit.status = 'declined'
    deposit.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=deposit.user,
        amount=deposit.amount,
        transaction_type='deposit',
        direction='credit',
        description=f"Declined {deposit.method} deposit",
        reference=generate_reference(),
        status="failed",

        beneficiary_name="****self",
        beneficiary_number="******self",
        bank_name="Dew Trust Bank",
    )

    # Notification
    create_notification(
        user=deposit.user,
        title="Deposit Declined",
        message=f"Your deposit of {deposit.user.bank_account.get_currency_symbol()}{deposit.amount} was declined.",
        notif_type="error",
        related_object=deposit
    )

    messages.warning(
        request,
        'Deposit declined.'
    )

    return redirect('staff:pending_transactions')


@login_required
@staff_required
@transaction.atomic
def approve_local_transfer(request, pk):

    transfer = get_object_or_404(
        LocalTransfer,
        pk=pk,
        status='pending'
    )

    transfer.status = 'successful'
    transfer.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=transfer.user,
        amount=transfer.amount,
        transaction_type='local_transfer',
        direction='debit',
        description=f"Approved local transfer to {transfer.beneficiary_name}",
        reference=generate_reference(),
        status="successful",

        beneficiary_name=transfer.beneficiary_name,
        beneficiary_number=transfer.beneficiary_number,
        bank_name=transfer.bank_name,
    )

    # Notification
    create_notification(
        user=transfer.user,
        title="Transfer Approved",
        message=f"Your local transfer of {transfer.user.bank_account.get_currency_symbol()}{transfer.amount} was approved successfully.",
        notif_type="success",
        related_object=transfer
    )

    messages.success(
        request,
        'Local transfer approved.'
    )

    return redirect('staff:pending_transactions')


@login_required
@staff_required
@transaction.atomic
def decline_local_transfer(request, pk):

    transfer = get_object_or_404(
        LocalTransfer,
        pk=pk,
        status='pending'
    )

    bank_account = transfer.user.bank_account

    # Refund Balance
    bank_account.balance += transfer.amount
    bank_account.save()

    # Update Status
    transfer.status = 'failed'
    transfer.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=transfer.user,
        amount=transfer.amount,
        transaction_type='local_transfer',
        direction='credit',
        description=f"Refund for declined transfer to {transfer.beneficiary_name}",
        reference=generate_reference(),
        status="failed",

        beneficiary_name=transfer.beneficiary_name,
        beneficiary_number=transfer.beneficiary_number,
        bank_name=transfer.bank_name,
    )

    # Notification
    create_notification(
        user=transfer.user,
        title="Transfer Declined",
        message=f"Your local transfer of {bank_account.get_currency_symbol()}{transfer.amount} was declined and refunded.",
        notif_type="error",
        related_object=transfer
    )

    messages.warning(
        request,
        'Local transfer declined and refunded.'
    )

    return redirect('staff:pending_transactions')


@login_required
@staff_required
@transaction.atomic
def approve_wire_transfer(request, pk):

    wire = get_object_or_404(
        InternationalTransfer,
        pk=pk,
        status='pending'
    )

    wire.status = 'successful'
    wire.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=wire.user,
        amount=wire.amount,
        transaction_type='wire_transfer',
        direction='debit',
        description=f"Approved wire transfer to {wire.beneficiary_name}",
        reference=generate_reference(),
        status="successful",

        beneficiary_name=wire.beneficiary_name,
        beneficiary_number=wire.beneficiary_number,
        bank_name=wire.bank_name,
    )

    # Notification
    create_notification(
        user=wire.user,
        title="Wire Transfer Approved",
        message=f"Your wire transfer of {wire.user.bank_account.get_currency_symbol()}{wire.amount} was approved successfully.",
        notif_type="success",
        related_object=wire
    )

    messages.success(
        request,
        'Wire transfer approved.'
    )

    return redirect('staff:pending_transactions')


@login_required
@staff_required
@transaction.atomic
def decline_wire_transfer(request, pk):

    wire = get_object_or_404(
        InternationalTransfer,
        pk=pk,
        status='pending'
    )

    bank_account = wire.user.bank_account

    # Refund
    bank_account.balance += wire.amount
    bank_account.save()

    # Update Status
    wire.status = 'failed'
    wire.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=wire.user,
        amount=wire.amount,
        transaction_type='wire_transfer',
        direction='credit',
        description=f"Refund for declined wire transfer to {wire.beneficiary_name}",
        reference=generate_reference(),
        status="failed",

        beneficiary_name=wire.beneficiary_name,
        beneficiary_number=wire.beneficiary_number,
        bank_name=wire.bank_name,
    )

    # Notification
    create_notification(
        user=wire.user,
        title="Wire Transfer Declined",
        message=f"Your wire transfer of {bank_account.get_currency_symbol()}{wire.amount} was declined and refunded.",
        notif_type="error",
        related_object=wire
    )

    messages.warning(
        request,
        'Wire transfer declined and refunded.'
    )

    return redirect('staff:pending_transactions')


@login_required
@staff_required
def view_deposit_proof(request, pk):

    deposit = get_object_or_404(
        Deposit,
        pk=pk
    )

    context = {
        'deposit': deposit
    }

    return render(
        request,
        'staff/view_deposit_proof.html',
        context
    )