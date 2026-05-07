from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.conf import settings

from .forms import CustomUserRegistrationForm
from customer.forms import UserBankAccountForm
from customer.models import BankAccountType,UserBankAccount

def register_view(request):
    account_types = BankAccountType.objects.all()
    if request.method == 'POST':

        user_form = CustomUserRegistrationForm(request.POST)
        bank_form = UserBankAccountForm(request.POST)

        if user_form.is_valid() and bank_form.is_valid():

            try:
                with transaction.atomic():

                    # 1. Create user
                    user = user_form.save()

                    # 2. Create bank account but don't commit yet
                    account = bank_form.save(commit=False, user=user)
                    print(account.account_type)
                    account.save()

                    # 3. Login user
                    # login(request, user)

                    messages.success(
                        request,
                        'Account and bank profile created successfully!'
                    )

                    return redirect('frontend:home')

            except Exception as e:
                print(e) 
                messages.error(
                    request,
                    'Something went wrong while creating your account.'
                )

        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:
        user_form = CustomUserRegistrationForm()
        bank_form = UserBankAccountForm()

    return render(request, 'account/register.html', {
        'form': user_form,
        'bank_form': bank_form,
        'account_types': account_types,
    })

import random

def login_view(request):

    if request.user.is_authenticated:
        return redirect('customer:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        remember = request.POST.get('remember')

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_active:

                # Save OTP + user in session
                request.session['pin_user_id'] = user.id

                # session expiry handling
                if remember:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                else:
                    request.session.set_expiry(300)  # 5 min OTP window

                # messages.success(request, "OTP sent to your email/phone")

                return redirect('account:verify_pin')

            else:
                messages.error(request, 'Invalid email or password.')

        else:
            messages.error(request, 'Please provide both email and password.')

    return render(request, 'account/login.html')


from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from account.models import CustomUser
from customer.models import UserBankAccount


def pin_verify_view(request):

    pin_user_id = request.session.get('pin_user_id')

    if not pin_user_id:
        return redirect('account:login')

    try:
        user_account = UserBankAccount.objects.get(
            user_id=pin_user_id
        )

    except UserBankAccount.DoesNotExist:

        messages.error(
            request,
            "Bank account not found."
        )

        return redirect('account:login')

    if request.method == 'POST':

        entered_pin = (
            request.POST.get('desktop_otp')
            or request.POST.get('mobile_otp')
        )

        print(entered_pin)

        # CHECK HASHED PIN
        if user_account.check_transaction_pin(entered_pin):

            try:
                user = CustomUser.objects.get(
                    id=pin_user_id
                )

            except CustomUser.DoesNotExist:

                messages.error(
                    request,
                    "User not found."
                )

                return redirect('account:login')

            # LOGIN USER
            login(request, user)

            # CLEAN SESSION
            request.session.pop('pin_user_id', None)

            messages.success(
                request,
                "Login successful!"
            )

            return redirect('customer:dashboard')

        else:

            messages.error(
                request,
                "Invalid verification pin. pleasze try again."
            )

    return render(
        request,
        'account/verify_pin.html',
        {
            'user_account': user_account
        }
    )


def logout_view(request):
    logout(request)  # clears user session completely
    messages.success(request, "You have been logged out successfully.")
    return redirect('account:login')