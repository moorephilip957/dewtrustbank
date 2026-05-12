from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .decorators import staff_required
from customer.models import UserBankAccount
from transaction.models import (
    Deposit,
    LocalTransfer,
    InternationalTransfer
)


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