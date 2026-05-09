from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import UserBankAccount, DebitCard
from .forms import DebitCardApplicationForm
from transaction.models import TransactionHistory


@login_required
def dashboard(request):
    bank_account = UserBankAccount.objects.select_related('user').get(
                        user=request.user
                    )
    context = {
        'bank_account': bank_account,
    }
    return render(
        request,
        'customer/dashboard.html',
        context
    )

@login_required
def transaction_list(request):

    transactions = TransactionHistory.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'customer/transactions.html',
        {
            'transactions': transactions
        }
    )


@login_required
def card(request):

    account = request.user.bank_account

    cards = DebitCard.objects.filter(
        account=account
    ).order_by('-created_at')

    active_cards_count = cards.filter(
        status='active'
    ).count()

    pending_cards_count = cards.filter(
        status='pending'
    ).count()

    blocked_cards_count = cards.filter(
        status='blocked'
    ).count()

    return render(
        request,
        'customer/cards.html',
        {
            'cards': cards,
            'active_cards_count': active_cards_count,
            'pending_cards_count': pending_cards_count,
            'blocked_cards_count': blocked_cards_count,
        }
    )


@login_required
def local_transfer(request):

    return render(
        request,
        'customer/local_transfer.html',
    )


@login_required
def international_transfer(request):

    return render(
        request,
        'customer/international_transfer.html',
    )


@login_required
def deposit(request):

    return render(
        request,
        'customer/deposit.html',
    )


@login_required
def save_invest(request):

    return render(
        request,
        'customer/save_invest.html',
    )


@login_required
def loan(request):

    return render(
        request,
        'customer/loan.html',
    )


@login_required
def loan_history(request):

    return render(
        request,
        'customer/loan_history.html',
    )


@login_required
def download_app(request):

    return render(
        request,
        'customer/download_app.html',
    )


@login_required
def settings(request):

    return render(
        request,
        'customer/settings.html',
    )


@login_required
def support(request):

    return render(
        request,
        'customer/support.html',
    )



@login_required
def change_password(request):

    return render(
        request,
        'customer/change_password.html',
    )


@login_required
def apply_card(request):

    account = request.user.bank_account

    if request.method == 'POST':

        form = DebitCardApplicationForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            # save application
            application = form.save(commit=False)
            application.account = account
            application.save()

            # create actual debit card
            DebitCard.objects.create(
                account=account,
                card_type=application.card_type,
                currency=application.currency,
                spending_limit=application.spending_limit,
                issuance_fee=application.issuance_fee,
                card_holder_name=request.user.get_full_name(),
                is_virtual=False,
                status='pending',
            )
            messages.success(request, 'Your debit card application has been successfully submitted and is currently pending approval and activation.')
            return redirect('customer:cards')

    else:

        form = DebitCardApplicationForm(
            user=request.user
        )

    return render(
        request,
        'customer/apply_card.html',
        {
            'form': form,
            'account': account,
        }
    )

@login_required
def payment(request):

    return render(
        request,
        'customer/crypto_payment.html',
    )