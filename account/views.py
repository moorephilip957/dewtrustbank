from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import transaction
from django.conf import settings

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

    # Redirect if already authenticated
    if request.user.is_authenticated:
        return redirect('customer:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        remember = request.POST.get('remember')

        if email and password:
            # Since USERNAME_FIELD = 'email', authenticate expects email=
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Welcome back! You are now signed in.')
                    
                    # Handle "Remember Me" session persistence
                    if remember:
                        request.session.set_expiry(settings.SESSION_COOKIE_AGE)  # ~2 weeks
                    else:
                        request.session.set_expiry(0)

                    # Redirect to ?next= or default dashboard
                    next_url = request.GET.get('next')
                    return redirect(next_url) if next_url else redirect('customer:dashboard')
                else:
                    messages.error(request, 'Your account has been disabled. Contact support.')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            messages.error(request, 'Please provide both email and password.')
    return render(request, 'account/login.html')
