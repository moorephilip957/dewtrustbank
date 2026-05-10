from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .forms import LocalTransferForm, InternationalTransferForm, DepositCreateForm, DepositProofForm
from .services import create_transaction
from customer.models import UserBankAccount
from .models import TransactionHistory, Deposit, CryptoWallet
from .utils import generate_reference

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
        form = InternationalTransferForm(user=request.user)

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


@login_required
def create_deposit(request):

    if request.method == "POST":

        form = DepositCreateForm(request.POST)

        if form.is_valid():

            deposit = form.save(commit=False)

            deposit.user = request.user
            deposit.save()

            return redirect(
                "transaction:deposit_detail",
                deposit_id=deposit.id
            )

    else:

        form = DepositCreateForm()

    return render(
        request,
        "transactions/create_deposit.html",
        {
            "form": form
        }
    )


@login_required
def deposit_detail(request, deposit_id):

    deposit = get_object_or_404(
        Deposit,
        id=deposit_id,
        user=request.user
    )

    wallet = None
    form = None

    # =========================
    # CRYPTO DEPOSITS
    # =========================

    if deposit.method in ["BTC", "USDT"]:

        wallet = CryptoWallet.objects.filter(
            currency=deposit.method,
            active=True
        ).first()

        # =========================
        # PROOF FORM
        # =========================

        if request.method == "POST":

            form = DepositProofForm(
                request.POST,
                request.FILES,
                instance=deposit
            )

            if form.is_valid():

                form.save()

                TransactionHistory.objects.create(
                user=request.user,
                amount=deposit.amount,
                transaction_type='deposit',
                direction='credit',
                description="**** self deposit",
                reference=generate_reference(),
                status="pending",

                # Beneficiary Details
                beneficiary_name="****self",
                beneficiary_number="******self",
                bank_name="Dew Trust Bank",
                )


                return redirect(
                    "transaction:deposit_pending",
                    deposit_id=deposit.id
                )

        else:

            form = DepositProofForm(
                instance=deposit
            )

    # =========================
    # WIRE TRANSFER
    # =========================

    elif deposit.method == "WIRE":

        # No form
        # Just instructions message

        form = None

    return render(
        request,
        "transactions/deposit_detail.html",
        {
            "deposit": deposit,
            "wallet": wallet,
            "form": form
        }
    )


@login_required
def deposit_pending(request, deposit_id):

    deposit = get_object_or_404(
        Deposit,
        id=deposit_id,
        user=request.user
    )

    return render(
        request,
        "transactions/deposit_pending.html",
        {
            "deposit": deposit
        }
    )