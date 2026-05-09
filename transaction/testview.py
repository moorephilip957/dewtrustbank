from django.shortcuts import redirect, render


def local_transfer_view(request):

    if request.method == "POST":

        form = LocalTransferForm(request.POST, user=request.user)

        if form.is_valid():

            data = form.cleaned_data
            account = Account.objects.get(user=request.user)

            result = create_transaction(
                user=request.user,
                account=account,
                amount=data["amount"],
                transaction_type="local_transfer",
                direction="debit",
                description=data["description"]
            )

            # 🎯 REDIRECT BASED ON RESULT

            if result.status == "success":
                return redirect("transfer_success", tx_id=result.transaction.id)

            elif result.status == "pending":
                return redirect("transfer_pending", tx_id=result.transaction.id)

            else:
                return redirect("transfer_failed", tx_id=result.transaction.id)

    else:
        form = LocalTransferForm(user=request.user)

    return render(request, "transfer.html", {"form": form})