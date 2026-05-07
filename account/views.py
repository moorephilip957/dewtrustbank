from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import CustomUserRegistrationForm
from customer.forms import UserBankAccountForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction

from .forms import CustomUserRegistrationForm
from customer.forms import UserBankAccountForm
from customer.models import BankAccountType

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

def login_view(request):
    return render(request, 'account/login.html')
