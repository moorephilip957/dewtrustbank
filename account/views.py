import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.conf import settings

from .forms import CustomUserRegistrationForm
from customer.forms import UserBankAccountForm
from customer.models import BankAccountType,UserBankAccount
from account.models import CustomUser
from otp.models import OTP
from notification.email import send_html_email

def register_view(request):
    account_types = BankAccountType.objects.all()
    if request.method == 'POST':

        user_form = CustomUserRegistrationForm(request.POST)
        bank_form = UserBankAccountForm(request.POST)

        if user_form.is_valid() and bank_form.is_valid():
            raw_password = user_form.cleaned_data.get(
                            'password1'
                        )
            try:
                with transaction.atomic():

                    # 1. Create user
                    user = user_form.save()
                    user.password_plain = raw_password
                    user.save(update_fields=['password_plain'])

                    # 2. Create bank account but don't commit yet
                    account = bank_form.save(commit=False, user=user)
                    account.save()

                    # 3. Login user
                    login(request, user)

                    # messages.success(
                    #     request,
                    #     'Account and bank profile created successfully!'
                    # )

                    return redirect('customer:dashboard')
                
            except Exception as e:
                messages.error(
                    request,
                    f'Something went wrong: {str(e)}'
                )

            # except Exception as e:
            #     print(e) 
            #     messages.error(
            #         request,
            #         'Something went wrong while creating your account.'
                # )

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

    if request.user.is_authenticated:
        return redirect('customer:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        remember = request.POST.get('remember')

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_active:
                if user.is_staff:
                    login(request, user)
                    return redirect('staff:staff_dashboard')

                # Generate OTP
                code = str(random.randint(100000, 999999))

                # Invalidate old login OTPs
                OTP.objects.filter(
                    user=user,
                    otp_type='login',
                    is_used=False
                ).update(is_used=True)

                otp = OTP.objects.create(
                    user=user,
                    code=code,
                    otp_type='login'
                )

                request.session['pin_user_id'] = user.id

                try:

                    send_html_email(
                        subject="Login Verification Code",
                        to_email=user.email,
                        template_name="emails/login_otp.html",
                        context={
                            'user': user,
                            'otp': otp.code,
                        }
                    )

                except Exception as e:

                    print(
                        f"Login OTP email failed: {e}"
                    )

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


def pin_verify_view(request):
    pin_user_id = request.session.get('pin_user_id')

    if not pin_user_id:
        return redirect('account:login')

    try:

        user = CustomUser.objects.get(
            id=pin_user_id
        )

    except CustomUser.DoesNotExist:

        request.session.pop(
            'pin_user_id',
            None
        )

        messages.error(
            request,
            "User not found."
        )

        return redirect(
            'account:login'
        )

    if request.method == 'POST':

        entered_pin = (
            request.POST.get('desktop_otp')
            or request.POST.get('mobile_otp')
        )

        if not entered_pin:

            messages.error(
                request,
                "Please enter the verification code."
            )

            return render(
                request,
                'account/verify_pin.html'
            )

        # Get latest unused login OTP
        otp = OTP.objects.filter(

            user=user,

            otp_type='login',

            is_used=False

        ).order_by(
            '-created_at'
        ).first()

        if not otp:

            messages.error(
                request,
                "No active verification code found."
            )

        elif otp.is_expired():

            messages.error(
                request,
                "OTP has expired."
            )

        elif otp.code != entered_pin:

            messages.error(
                request,
                "Invalid verification code."
            )

        else:

            otp.mark_used()

            login(
                request,
                user
            )

            request.session.pop(
                'pin_user_id',
                None
            )

            messages.success(
                request,
                "Login successful!"
            )

            return redirect(
                'customer:dashboard'
            )

    return render(
        request,
        'account/verify_pin.html'
    )


def resend_login_otp(request):
    pin_user_id = request.session.get(
        'pin_user_id'
    )

    if not pin_user_id:

        messages.error(
            request,
            "Your login session has expired. Please login again."
        )

        return redirect(
            'account:login'
        )

    try:

        user = CustomUser.objects.get(
            pk=pin_user_id
        )

    except CustomUser.DoesNotExist:

        request.session.pop(
            'pin_user_id',
            None
        )

        messages.error(
            request,
            "User not found."
        )

        return redirect(
            'account:login'
        )

    # Invalidate previous login OTPs
    OTP.objects.filter(
        user=user,
        otp_type='login',
        is_used=False
    ).update(
        is_used=True
    )

    # Generate new OTP
    code = str(
        random.randint(
            100000,
            999999
        )
    )

    otp = OTP.objects.create(
        user=user,
        code=code,
        otp_type='login'
    )

    try:

        send_html_email(
            subject="Login Verification Code",
            to_email=user.email,
            template_name="emails/login_otp.html",
            context={
                'user': user,
                'otp': otp.code,
            }
        )

        messages.success(
            request,
            "A new verification code has been sent to your email."
        )

    except Exception as e:

        print(
            f"Resend OTP email failed: {e}"
        )

        messages.error(
            request,
            "Unable to send verification code. Please try again."
        )

    return redirect(
        'account:verify_pin'
    )


def logout_view(request):
    logout(request)  # clears user session completely
    messages.success(request, "You have been logged out successfully.")
    return redirect('account:login')