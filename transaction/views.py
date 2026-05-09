from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .forms import LocalTransferForm, InternationalTransferForm
from .services import create_transaction
from customer.models import UserBankAccount
from .models import TransactionHistory

@login_required
def local_transfer(request):
    if request.method == "POST":

        form = LocalTransferForm(request.POST, user=request.user)

        if form.is_valid():

            data = form.cleaned_data
            account = UserBankAccount.objects.get(user=request.user)

            result = create_transaction(
                user=request.user,
                account=account,
                amount=data["amount"],
                transaction_type="local_transfer",
                direction="debit",
                description=data["description"],
                beneficiary_name=data["beneficiary_name"],
                beneficiary_number=data["beneficiary_number"],
                bank_name=data["bank_name"],
            )


            if result.status == "success":
                return redirect("transaction:transfer_success", tx_id=result.transaction.id)

            elif result.status == "pending":
                return redirect("transaction:transfer_pending", tx_id=result.transaction.id)

            else:
                return redirect("transaction:transfer_failed", tx_id=result.transaction.id)

    else:
        form = LocalTransferForm(user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'transactions/local_transfer.html', context)


@login_required
def wire_transfer(request):
    if request.method == 'POST':
        form = InternationalTransferForm(request.POST, user=request.user)

        if form.is_valid():

            data = form.cleaned_data
            account = UserBankAccount.objects.get(user=request.user)

            result = create_transaction(
                user=request.user,
                account=account,
                amount=data["amount"],
                transaction_type="wire_transfer",
                direction="debit",
                description=data["description"],
                beneficiary_name=data["beneficiary_name"],
                beneficiary_number=data["beneficiary_number"],
                bank_name=data["bank_name"],
            )

            if result.status == "success":
                return redirect("transaction:transfer_success", tx_id=result.transaction.id)

            elif result.status == "pending":
                return redirect("transaction:transfer_pending", tx_id=result.transaction.id)

            else:
                return redirect("transaction:transfer_failed", tx_id=result.transaction.id)
    else:
        form = InternationalTransferForm(request.POST, user=request.user)

    context = {
        'form': form,
    }
    return render(
        request,
        'transactions/wire_transfer.html',
        context
    )


@login_required
def transfer_success(request, tx_id):

    transaction = get_object_or_404(
        TransactionHistory,
        id=tx_id,
        user=request.user
    )

    return render(
        request,
        "transactions/transfer_success.html",
        {
            "transaction": transaction
        }
    )

@login_required
def transfer_pending(request, tx_id):

    transaction = get_object_or_404(
        TransactionHistory,
        id=tx_id,
        user=request.user
    )

    return render(
        request,
        "transactions/transfer_pending.html",
        {
            "transaction": transaction
        }
    )


@login_required
def transfer_failed(request, tx_id):

    transaction = get_object_or_404(
        TransactionHistory,
        id=tx_id,
        user=request.user
    )

    return render(
        request,
        "transactions/transfer_failed.html",
        {
            "transaction": transaction
        }
    )