from django.shortcuts import render, redirect

from .forms import LocalTransferForm
from .services import create_transaction
from customer.models import UserBankAccount

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
                description=data["description"]
            )

            return redirect('transaction:local_transfer')

            # if result.status == "success":
            #     return redirect("transfer_success", tx_id=result.transaction.id)

            # elif result.status == "pending":
            #     return redirect("transfer_pending", tx_id=result.transaction.id)

            # else:
            #     return redirect("transfer_failed", tx_id=result.transaction.id)

    else:
        form = LocalTransferForm(user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'transactions/local_transfer.html', context)
