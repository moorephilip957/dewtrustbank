from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import UserBankAccount


@login_required
def dashboard(request):

    return render(
        request,
        'customer/dashboard.html',
    )

@login_required
def transaction_list(request):

    return render(
        request,
        'customer/transactions.html',
    )

@login_required
def card(request):

    return render(
        request,
        'customer/cards.html',
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

    return render(
        request,
        'customer/apply_card.html',
    )


@login_required
def payment(request):

    return render(
        request,
        'customer/crypto_payment.html',
    )