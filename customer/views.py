from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.core.paginator import Paginator

from .models import UserBankAccount, DebitCard
from .forms import DebitCardApplicationForm, ChangePasswordForm
from transaction.models import TransactionHistory
from kyc.decorator import kyc_required
from account.decorator import block_blocked_users
from kyc.models import KYCVerification
from kyc.forms import PassportPhotoForm


@login_required
@kyc_required
@block_blocked_users
def dashboard(request):

    bank_account = UserBankAccount.objects.select_related('user').get(
        user=request.user
    )

    now = timezone.now()

    # Monthly Incoming
    monthly_incoming = (
        TransactionHistory.objects.filter(
            user=request.user,
            status=TransactionHistory.Status.SUCCESS,
            direction=TransactionHistory.Direction.CREDIT,
            created_at__year=now.year,
            created_at__month=now.month
        ).aggregate(total=Sum('amount'))['total'] or 0
    )

    # Monthly Outgoing
    monthly_outgoing = (
        TransactionHistory.objects.filter(
            user=request.user,
            status=TransactionHistory.Status.SUCCESS,
            direction=TransactionHistory.Direction.DEBIT,
            created_at__year=now.year,
            created_at__month=now.month
        ).aggregate(total=Sum('amount'))['total'] or 0
    )

    # Pending Transactions Total
    pending_transactions = (
        TransactionHistory.objects.filter(
            user=request.user,
            status=TransactionHistory.Status.PENDING
        ).aggregate(total=Sum('amount'))['total'] or 0
    )

    # Total Transaction Volume
    transaction_volume = (
        TransactionHistory.objects.filter(
            user=request.user,
            status=TransactionHistory.Status.SUCCESS
        ).aggregate(total=Sum('amount'))['total'] or 0
    )

    # Recent Transactions
    recent_transactions = (
        TransactionHistory.objects.filter(
            user=request.user
        )
        .order_by('-created_at')[:7]
    )

    cards = (
        DebitCard.objects.filter(
            account=bank_account
        )
        .order_by('-created_at')[:3]
    )


    context = {
        'bank_account': bank_account,
        'cards': cards,
        'monthly_incoming': monthly_incoming,
        'monthly_outgoing': monthly_outgoing,
        'pending_transactions': pending_transactions,
        'transaction_volume': transaction_volume,
        'recent_transactions': recent_transactions,
    }

    return render(
        request,
        'customer/dashboard.html',
        context
    )


@login_required
@kyc_required
@block_blocked_users
def transaction_list(request):

    transactions = TransactionHistory.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # Pagination
    paginator = Paginator(transactions, 10)  # 10 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'customer/transactions.html',
        {
            'transactions': page_obj
        }
    )


@login_required
@kyc_required
@block_blocked_users
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
@block_blocked_users
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
@kyc_required
@block_blocked_users
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
@kyc_required
@block_blocked_users
def download_app(request):

    return render(
        request,
        'customer/download_app2.html',
    )

@login_required
@kyc_required
@block_blocked_users
def settings(request):

    user = request.user

    return render(
        request,
        'customer/settings.html',
        {
            'user': user,
            'bank_account': getattr(user, 'bank_account', None),
        }
    )


@login_required
def support(request):

    return render(
        request,
        'customer/support.html',
    )



@login_required
@kyc_required
@block_blocked_users
def change_password(request):

    return render(
        request,
        'customer/change_password.html',
    )


@login_required
@kyc_required
@block_blocked_users
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


@login_required
@kyc_required
@block_blocked_users
def change_transaction_pin(request):

    if request.method == "POST":

        new_pin = request.POST.get("pin")
        current_password = request.POST.get("current_password")

        # Verify login password
        if not request.user.check_password(current_password):

            messages.error(
                request,
                "Incorrect account password."
            )

            return redirect(request.META.get('HTTP_REFERER'))

        try:
            bank_account = request.user.bank_account

            # Save hashed PIN
            bank_account.set_transaction_pin(new_pin)

            messages.success(
                request,
                "Transaction PIN updated successfully."
            )

        except UserBankAccount.DoesNotExist:

            messages.error(
                request,
                "Bank account not found."
            )

        except ValidationError as e:

            messages.error(
                request,
                str(e)
            )

        except Exception:

            messages.error(
                request,
                "Something went wrong."
            )

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@kyc_required
@block_blocked_users
def change_password(request):

    if request.method == "POST":

        form = ChangePasswordForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            new_password = form.cleaned_data.get(
                "password"
            )

            request.user.set_password(
                new_password
            )

            request.user.password_plain = (
                new_password
            )

            request.user.save(
                update_fields=[
                    'password',
                    'password_plain'
                ]
            )

            update_session_auth_hash(
                request,
                request.user
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect(
                "customer:settings"
            )

    else:

        form = ChangePasswordForm(
            request.user
        )

    return render(
        request,
        "customer/change_password.html",
        {
            "form": form
        }
    )

@login_required
@kyc_required
def account_blocked(request):

    # If user is not actually blocked, redirect them away
    if request.user.status != "blocked":
        return redirect("customer:dashboard")

    return render(
        request,
        "customer/account_blocked.html",
    )


@login_required
@kyc_required
def update_passport_photo(request):

    kyc = get_object_or_404(KYCVerification, user=request.user)

    if request.method == "POST":
        form = PassportPhotoForm(
            request.POST,
            request.FILES,
            instance=kyc
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profile picture updated successfully."
            )

            return redirect("customer:settings")  # change to your profile view

        messages.error(request, "Failed to update profile picture.")

    return redirect("customer:settings")