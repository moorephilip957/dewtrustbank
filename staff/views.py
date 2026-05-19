from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.db.models import Sum, Count
from django.utils.timezone import now
from django.core.paginator import Paginator 

from transaction.models import (
    Deposit,
    LocalTransfer,
    InternationalTransfer,
    TransactionHistory,
)
from .forms import (
    CustomerUpdateForm,
    BankAccountUpdateForm,
    AccountAdjustmentForm,
    CopyTransactionHistoryForm,
)
from .models import AccountFunding
from transaction.utils import generate_reference
from account.models import CustomUser
from .decorators import staff_required
from customer.models import UserBankAccount, DebitCardApplication, DebitCard
from notification.utils import create_notification
from kyc.models import KYCVerification
from support.models import Ticket, TicketMessage
from .forms import TicketMessageForm
from loan.models import LoanApplication
from notification.email import send_html_email
from transaction.forms import TransactionHistoryForm


@login_required
@staff_required
def staff_dashboard(request):

    # =========================
    # COUNTS
    # =========================

    total_customers = CustomUser.objects.filter(
        is_staff=False
    ).count()

    total_deposits = Deposit.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_local_transfers = LocalTransfer.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_international_transfers = InternationalTransfer.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_transfers = (
        total_local_transfers +
        total_international_transfers
    )

    pending_kyc = KYCVerification.objects.filter(
        status='pending'
    ).count()

    # =========================
    # RECENT TRANSACTIONS
    # =========================

    recent_transactions = TransactionHistory.objects.select_related(
        'user'
    ).order_by('-created_at')[:20]

    # =========================
    # CONTEXT
    # =========================

    context = {

        'total_customers': total_customers,

        'total_deposits': total_deposits,

        'total_transfers': total_transfers,

        'pending_kyc': pending_kyc,

        'recent_transactions': recent_transactions,
    }

    return render(
        request,
        'staff/dashboard.html',
        context
    )


@login_required
@staff_required
def account_holders(request):

    customers = UserBankAccount.objects.select_related(
        'user'
    ).all().order_by('-id')

    context = {
        'customers': customers
    }

    return render(
        request,
        'staff/account_holders.html',
        context
    )


@login_required
@staff_required
def update_customer(request, pk):

    customer = get_object_or_404(
        UserBankAccount.objects.select_related('user'),
        pk=pk
    )

    user = customer.user

    user_form = CustomerUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=user
    )

    bank_form = BankAccountUpdateForm(
        request.POST or None,
        instance=customer
    )

    print(bank_form.fields.keys())

    if request.method == 'POST':

        if user_form.is_valid() and bank_form.is_valid():

            user_form.save()
            bank_form.save()

            messages.success(
                request,
                'Customer information updated successfully.'
            )

            return redirect(
                'staff:account_holders',
            )

    context = {
        'customer': customer,
        'user_form': user_form,
        'bank_form': bank_form,
    }

    return render(
        request,
        'staff/update_customer.html',
        context
    )


@login_required
@staff_required
def delete_customer(request, pk):

    customer = get_object_or_404(
        UserBankAccount,
        pk=pk
    )

    user = customer.user

    # Delete User
    # Bank account deletes automatically because of CASCADE
    user.delete()

    messages.success(
        request,
        'Customer account deleted successfully.'
    )

    return redirect('staff:account_holders')


@login_required
@staff_required
@transaction.atomic
def fund_customer(request):

    form = AccountAdjustmentForm(
        request.POST or None
    )

    # Change labels ONLY for credit view
    form.fields['beneficiary_name'].label = "Sender Name"
    form.fields['beneficiary_number'].label = "Sender Account / ID"
    form.fields['bank_name'].label = "Sender Bank"

    # Hide adjustment type from staff
    form.fields.pop('transaction_type')

    if request.method == 'POST':

        if form.is_valid():

            funding = form.save(commit=False)

            funding.staff = request.user

            funding.transaction_type = 'credit'

            funding.save()

            customer = funding.customer

            bank_account = customer.bank_account

            # Add Balance
            bank_account.balance += funding.amount
            bank_account.save()

            # Transaction History
            transaction = TransactionHistory.objects.create(
                user=customer,

                amount=funding.amount,

                transaction_type='deposit',

                direction='credit',

                description=(
                    funding.description
                    if funding.description
                    else '******** Deposit'
                ),

                reference=generate_reference(),

                status='success',

                beneficiary_name=funding.beneficiary_name,

                beneficiary_number=funding.beneficiary_number,

                bank_name=funding.bank_name,

                created_at=funding.transaction_date
            )

            try:
                send_html_email(
                    subject="Account Credited",
                    to_email=customer.email,
                    template_name="emails/credit_alert.html",
                    context={
                        'user': customer,
                        'amount': funding.amount,
                        'currency': bank_account.get_currency_symbol(),
                        'reference': transaction.reference,
                        'dashboard_url': 'https://www.firsthavinbk.com/account/dashboard/'
                    }
                )

            except Exception as e:

                print(f"Email sending failed: {e}")

            # Notification
            # create_notification(
            #     user=customer,

            #     title='Account Credited',

            #     message=(
            #         f'Your account has been credited with '
            #         f'{bank_account.get_currency_symbol()}'
            #         f'{funding.amount}.'
            #     ),

            #     notif_type='success',

            #     related_object=funding
            # )

            messages.success(
                request,
                'Customer funded successfully.'
            )

            return redirect(
                'staff:account_holders'
            )

    context = {
        'form': form,
        'page_title': 'Fund Customer Account',
        'button_text': 'Fund Customer',
    }

    return render(
        request,
        'staff/account_adjustment.html',
        context
    )


@login_required
@staff_required
@transaction.atomic
def debit_customer(request):

    form = AccountAdjustmentForm(
        request.POST or None
    )

    # Hide adjustment type
    form.fields.pop('transaction_type')

    if request.method == 'POST':

        if form.is_valid():

            debit = form.save(commit=False)

            debit.staff = request.user

            debit.transaction_type = 'debit'

            customer = debit.customer

            bank_account = customer.bank_account

            # Prevent overdraft
            if bank_account.balance < debit.amount:

                messages.error(
                    request,
                    'Insufficient customer balance.'
                )

                return redirect(
                    'staff:debit_customer'
                )

            debit.save()

            # Deduct Balance
            bank_account.balance -= debit.amount
            bank_account.save()

            # Transaction History
            transaction = TransactionHistory.objects.create(
                user=customer,

                amount=debit.amount,

                transaction_type='withdrawal',

                direction='debit',

                description=(
                    debit.description
                    if debit.description
                    else '******* withdrawal'
                ),

                reference=generate_reference(),

                status='success',

                beneficiary_name=debit.beneficiary_name,

                beneficiary_number=debit.beneficiary_number,

                bank_name=debit.bank_name,

                created_at=debit.transaction_date
            )

            try:
                send_html_email(
                    subject="Account Debited",
                    to_email=customer.email,
                    template_name="emails/debit_alert.html",
                    context={
                        'user': customer,
                        'amount': debit.amount,
                        'currency': bank_account.get_currency_symbol(),
                        'reference': transaction.reference,
                        'dashboard_url': 'https://www.firsthavinbk.com/account/dashboard/'
                    }
                )

            except Exception as e:

                print(f"Email sending failed: {e}")

            # Notification
            # create_notification(
            #     user=customer,

            #     title='Account Debited',

            #     message=(
            #         f'Your account has been debited with '
            #         f'{bank_account.get_currency_symbol()}'
            #         f'{debit.amount}.'
            #     ),

            #     notif_type='warning',

            #     related_object=debit
            # )

            messages.success(
                request,
                'Customer debited successfully.'
            )

            return redirect(
                'staff:account_holders'
            )

    context = {
        'form': form,
        'page_title': 'Debit Customer Account',
        'button_text': 'Debit Customer',
    }

    return render(
        request,
        'staff/account_adjustment.html',
        context
    )

@login_required
@staff_required
def kyc_requests(request):

    status = request.GET.get('status')

    kyc_qs = KYCVerification.objects.select_related('user')

    if status:
        kyc_qs = kyc_qs.filter(status=status)

    context = {
        'kyc_requests': kyc_qs.order_by('-created_at'),
        'status': status
    }

    return render(
        request,
        'staff/kyc_requests.html',
        context
    )

@login_required
@staff_required
def kyc_detail(request, pk):

    kyc = get_object_or_404(
        KYCVerification.objects.select_related('user'),
        pk=pk
    )

    context = {
        'kyc': kyc
    }

    return render(
        request,
        'staff/kyc_detail.html',
        context
    )


@login_required
@staff_required
def approve_kyc(request, pk):

    kyc = get_object_or_404(KYCVerification, pk=pk)

    kyc.status = 'approved'
    kyc.verified = True
    kyc.save()

    # Optional: update user status
    kyc.user.status = 'active'
    kyc.user.save()

    # Notification
    create_notification(
        user=kyc.user,
        title="KYC verification Approved",
        message = f"Your KYC verification has been successfully approved. You now have full access to all verified account features.",
        notif_type="info",
        related_object=kyc  
    )

    try:
        send_html_email(
            subject="KYC Verification Approved",
            to_email=kyc.user.email,
            template_name="emails/kyc_approved.html",
            context={
                'user': kyc.user,
                'dashboard_url': 'https://www.firsthavinbk.com/account/dashboard/'
            }
        )

    except Exception as e:

        print(f"Email sending failed: {e}")

    messages.success(request, 'KYC approved successfully.')

    return redirect('staff:kyc_requests')


@login_required
@staff_required
def reject_kyc(request, pk):

    kyc = get_object_or_404(KYCVerification, pk=pk)

    kyc.status = 'rejected'
    kyc.verified = False
    kyc.save()

    # Notification
    create_notification(
        user=kyc.user,
        title="KYC Verification Rejected",
        message = f"Your KYC verification was not approved. Please review your submitted documents and try again, or contact support for further assistance.",
        notif_type="info",
        related_object=kyc  
    )

    try:
        send_html_email(
            subject="KYC verification Rejected",
            to_email=kyc.user.email,
            template_name="emails/kyc_rejected.html",
            context={
                'user': kyc.user,
                'dashboard_url': 'https://www.firsthavinbk.com/account/dashboard/'
            }
        )

    except Exception as e:

        print(f"Email sending failed: {e}")

    messages.warning(request, 'KYC rejected.')

    return redirect('staff:kyc_requests')


@login_required
@staff_required
def ticket_list(request):

    status = request.GET.get('status')

    tickets = Ticket.objects.select_related('user').prefetch_related('messages')

    if status:
        tickets = tickets.filter(status=status)

    context = {
        'tickets': tickets.order_by('-updated_at'),
        'status': status
    }

    return render(
        request,
        'staff/ticket_list.html',
        context
    )


@login_required
@staff_required
def ticket_detail(request, pk):

    ticket = get_object_or_404(
        Ticket.objects.select_related('user').prefetch_related('messages'),
        pk=pk
    )

    form = TicketMessageForm()

    if request.method == "POST":

        form = TicketMessageForm(request.POST, request.FILES)

        if form.is_valid():

            message = form.save(commit=False)

            message.ticket = ticket
            message.sender = "support"

            message.save()

            # optional: update ticket status
            if ticket.status == "open":
                ticket.status = "in_progress"
                ticket.save()

            # =========================
            # NOTIFICATION TO CUSTOMER
            # =========================

            create_notification(
                user=ticket.user,

                title="New Support Response",

                message=(
                    f"Support has replied to your ticket "
                    f"({ticket.reference_id})."
                ),

                notif_type="info",

                related_object=ticket
            )
            try:
                send_html_email(
                    subject="New Support Response",
                    to_email=ticket.user.email,
                    template_name="emails/support_reply.html",
                    context={
                        "user": ticket.user,
                        "ticket": ticket,
                        "reply": message.content,
                        "ticket_url": f"https://firsthavinbk.com/support/tickets/{ticket.id}/",
                    }
                )
            except Exception as e:
                print(f"Email sending failed: {e}")

            return redirect('staff:ticket_detail', pk=ticket.pk)

    context = {
        'ticket': ticket,
        'form': form
    }

    return render(
        request,
        'staff/ticket_detail.html',
        context
    )


@login_required
@staff_required
def card_applications(request):

    status = request.GET.get('status')

    cards = DebitCard.objects.select_related(
        'account',
        'account__user'
    )

    if status:
        cards = cards.filter(status=status)

    context = {
        'cards': cards.order_by('-created_at'),
        'status': status
    }

    return render(
        request,
        'staff/card_applications.html',
        context
    )


@login_required
@staff_required
def approve_card_application(request, pk):

    card = get_object_or_404(
        DebitCard,
        pk=pk
    )

    # =========================
    # ACTIVATE CARD
    # =========================

    card.status = 'active'
    card.save()

    # =========================
    # NOTIFICATION
    # =========================

    create_notification(
        user=card.account.user,

        title="Debit Card Activated",

        message=(
            "Your debit card has been approved "
            "and activated successfully."
        ),

        notif_type="success",

        related_object=card
    )


    # email
    try:
        send_html_email(
            subject="Debit Card Activated",
            to_email=card.account.user.email,
            template_name="emails/card_activated.html",
            context={
                "user": card.account.user,
                "card": card,
                "last4": card.card_number[-4:],
            }
        )
    except Exception as e:
        print(f"Email sending failed: {e}")

    messages.success(
        request,
        'Card approved successfully.'
    )

    return redirect('staff:card_applications')


@login_required
@staff_required
def decline_card_application(request, pk):

    card = get_object_or_404(
        DebitCard,
        pk=pk
    )

    # =========================
    # BLOCK / DECLINE CARD
    # =========================

    card.status = 'blocked'
    card.save()

    # =========================
    # NOTIFICATION
    # =========================

    create_notification(
        user=card.account.user,

        title="Debit Card Declined",

        message=(
            "Your debit card application "
            "was declined."
        ),

        notif_type="warning",

        related_object=card
    )

    messages.warning(
        request,
        'Card application declined.'
    )

    return redirect('staff:card_applications')


@login_required
@staff_required
def deactivate_card(request, pk):

    card = get_object_or_404(
        DebitCard,
        pk=pk
    )

    # =========================
    # BLOCK CARD
    # =========================

    card.status = 'blocked'
    card.save()

    # =========================
    # NOTIFICATION
    # =========================

    create_notification(
        user=card.account.user,

        title="Debit Card Deactivated",

        message=(
            "Your debit card has been "
            "temporarily deactivated."
        ),

        notif_type="warning",

        related_object=card
    )

    messages.warning(
        request,
        'Card deactivated successfully.'
    )

    return redirect('staff:card_applications')


@login_required
@staff_required
def activate_card(request, pk):

    card = get_object_or_404(
        DebitCard,
        pk=pk
    )

    # =========================
    # ACTIVATE CARD
    # =========================

    card.status = 'active'
    card.save()

    # =========================
    # CREATE NOTIFICATION
    # =========================

    create_notification(
        user=card.account.user,

        title="Debit Card Activated",

        message=(
            "Your debit card has been "
            "activated successfully."
        ),

        notif_type="success",

        related_object=card
    )

    # =========================
    # DJANGO MESSAGE
    # =========================

    messages.success(
        request,
        'Card activated successfully.'
    )

    return redirect('staff:card_applications')


@login_required
@staff_required
def loan_applications(request):

    status = request.GET.get('status')

    loans = LoanApplication.objects.select_related(
        'applicant',
        'applicant__bank_account'
    )

    if status:
        loans = loans.filter(status=status)

    context = {
        'loans': loans.order_by('-date_applied'),
        'status': status
    }

    return render(
        request,
        'staff/loans/loan_applications.html',
        context
    )


@login_required
@staff_required
def process_loan(request, pk):

    loan = get_object_or_404(
        LoanApplication,
        pk=pk
    )

    loan.status = 'processing'
    loan.save()

    create_notification(
        user=loan.applicant,

        title="Loan Processing",

        message=(
            "Your loan application "
            "is currently under review."
        ),

        notif_type="info",

        related_object=loan
    )

    messages.info(
        request,
        'Loan moved to processing.'
    )

    return redirect('staff:loan_applications')


@login_required
@staff_required
def approve_loan(request, pk):

    loan = get_object_or_404(
        LoanApplication.objects.select_related(
            'applicant',
            'applicant__bank_account'
        ),
        pk=pk
    )

    # prevent duplicate disbursement
    if loan.status == 'disbursed':

        messages.warning(
            request,
            'Loan already disbursed.'
        )

        return redirect('staff:loan_applications')

    account = loan.applicant.bank_account

    # =========================
    # CREDIT ACCOUNT
    # =========================

    account.balance += loan.amount
    account.save()

    # =========================
    # UPDATE LOAN STATUS
    # =========================

    loan.status = 'disbursed'
    loan.save()

    # =========================
    # CREATE TRANSACTION HISTORY
    # =========================

    TransactionHistory.objects.create(

        user=loan.applicant,

        amount=loan.amount,

        transaction_type='loan',

        direction='credit',

        description=(
            f"Loan disbursement "
            f"({loan.loan_type})"
        ),

        reference=generate_reference(),

        status='success',

        beneficiary_name='Loan Department',

        beneficiary_number='LOAN-001',

        bank_name='First Havin Bank',
    )

    # =========================
    # NOTIFICATION
    # =========================

    create_notification(
        user=loan.applicant,

        title="Loan Approved",

        message=(
            f"Your loan of "
            f"{account.get_currency_symbol()}"
            f"{loan.amount} has been disbursed."
        ),

        notif_type="success",

        related_object=loan
    )


    # =========================
    # EMAIL ALERT
    # =========================

    try:

        send_html_email(

            subject="Loan Disbursed Successfully",

            to_email=loan.applicant.email,

            template_name="emails/loan_approved.html",

            context={

                'user': loan.applicant,

                'amount': loan.amount,

                'currency': account.get_currency_symbol(),

                'duration': loan.duration_months,

                'repayment': loan.total_repayment,

                'dashboard_url': (
                    'https://www.firsthavinbk.com/'
                    'account/dashboard/'
                )
            }

        )

    except Exception as e:

        print(
            f"Loan approval email failed: {e}"
        )

    messages.success(
        request,
        'Loan approved and disbursed.'
    )

    return redirect('staff:loan_applications')


@login_required
@staff_required
def reject_loan(request, pk):

    loan = get_object_or_404(
        LoanApplication,
        pk=pk
    )

    loan.status = 'rejected'
    loan.save()

    create_notification(
        user=loan.applicant,

        title="Loan Rejected",

        message=(
            "Your loan application "
            "was rejected."
        ),

        notif_type="warning",

        related_object=loan
    )

    messages.warning(
        request,
        'Loan rejected.'
    )

    return redirect('staff:loan_applications')


@login_required
@staff_required
def customer_details(request, pk):

    customer = get_object_or_404(
        UserBankAccount.objects.select_related('user'),
        pk=pk
    )

    # Deposits
    deposits = Deposit.objects.filter(
        user=customer.user
    ).order_by('-created_at')

    # Transaction history
    history = TransactionHistory.objects.filter(
        user=customer.user
    ).order_by('-created_at')

    # Paginate history
    paginator = Paginator(history, 10)  # 10 items per page
    page_number = request.GET.get('page')
    history_page = paginator.get_page(page_number)

    context = {
        'customer': customer,
        'deposits': deposits,
        'history': history_page,
    }

    return render(
        request,
        'staff/customer_details.html',
        context
    )


@login_required
@staff_required
def edit_history(request, pk):

    history = get_object_or_404(
        TransactionHistory,
        pk=pk
    )

    form = TransactionHistoryForm(
        request.POST or None,
        instance=history
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Transaction history updated successfully.'
        )

        return redirect(
            'staff:customer_details',
            pk=history.user.bank_account.pk
        )

    context = {
        'form': form,
        'history': history
    }

    return render(
        request,
        'staff/edit_history.html',
        context
    )

@login_required
@staff_required
def delete_history(request, pk):

    history = get_object_or_404(
        TransactionHistory,
        pk=pk
    )

    customer_pk = history.user.bank_account.pk

    history.delete()

    messages.success(request, 'Transaction history deleted successfully.')

    return redirect('staff:customer_details', pk=customer_pk)


@login_required
@staff_required
def pending_transactions(request):

    deposits = Deposit.objects.filter(
        status='pending'
    ).select_related('user').order_by('-created_at')

    local_transfers = LocalTransfer.objects.filter(
        status='pending'
    ).select_related('user').order_by('-created_at')

    wire_transfers = InternationalTransfer.objects.filter(
        status='pending'
    ).select_related('user').order_by('-created_at')

    context = {
        'deposits': deposits,
        'local_transfers': local_transfers,
        'wire_transfers': wire_transfers,
    }

    return render(
        request,
        'staff/pending_transactions.html',
        context
    )


@login_required
@staff_required
def toggle_sms_alert(request, pk):

    user = get_object_or_404(
        CustomUser,
        pk=pk
    )

    # Toggle SMS Alert
    if user.sms_alert == 'activate':
        user.sms_alert = 'deactivate'
        messages.success(
            request,
            'SMS alert deactivated successfully.'
        )

    else:
        user.sms_alert = 'activate'
        messages.success(
            request,
            'SMS alert activated successfully.'
        )

    user.save()

    return redirect(
        'staff:customer_details',
        pk=user.bank_account.pk
    )


@login_required
@staff_required
def toggle_account_status(request, pk):

    user = get_object_or_404(
        CustomUser,
        pk=pk
    )

    # =========================
    # BLOCK ACCOUNT
    # =========================

    if user.status == 'active':

        user.status = 'blocked'
        user.save()

        # =========================
        # NOTIFICATION
        # =========================

        create_notification(

            user=user,

            title="Account Restricted",

            message=(
                "Your account has been temporarily "
                "restricted. Please contact support "
                "for assistance."
            ),

            notif_type="warning"
        )

        # =========================
        # EMAIL ALERT
        # =========================

        try:

            send_html_email(

                subject="Account Restricted",

                to_email=user.email,

                template_name="emails/account_blocked.html",

                context={
                    'user': user,
                    'dashboard_url': (
                        'https://www.firsthavinbk.com/'
                        'account/dashboard/'
                    )
                }
            )

        except Exception as e:

            print(
                f"Blocked account email failed: {e}"
            )

        messages.warning(
            request,
            'Customer account has been blocked.'
        )

    # =========================
    # ACTIVATE ACCOUNT
    # =========================

    else:

        user.status = 'active'
        user.save()

        # =========================
        # NOTIFICATION
        # =========================

        create_notification(

            user=user,

            title="Account Unblocked",

            message=(
                "Your account has been activated "
                "successfully. You may now continue "
                "using banking services."
            ),

            notif_type="success"
        )

        # =========================
        # EMAIL ALERT
        # =========================

        try:

            send_html_email(

                subject="Account Activated",

                to_email=user.email,

                template_name="emails/account_unblocked.html",

                context={
                    'user': user,
                    'dashboard_url': (
                        'https://www.firsthavinbk.com/'
                        'account/dashboard/'
                    )
                }
            )

        except Exception as e:

            print(
                f"Account activation email failed: {e}"
            )

        messages.success(
            request,
            'Customer account has been activated.'
        )

    return redirect(
        'staff:customer_details',
        pk=user.bank_account.pk
    )


@login_required
@staff_required
def change_customer_password(request, pk):

    user = get_object_or_404(
        CustomUser,
        pk=pk
    )

    if request.method == 'POST':

        password = request.POST.get('password')
        confirm_password = request.POST.get(
            'confirm_password'
        )

        # Validate
        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect(
                'staff:customer_details',
                pk=user.bank_account.pk
            )

        # Set Password
        user.set_password(password)

        user.save()

        messages.success(
            request,
            'Customer password changed successfully.'
        )

        return redirect(
            'staff:customer_details',
            pk=user.bank_account.pk
        )

    return redirect(
        'staff:customer_details',
        pk=user.bank_account.pk
    )


# transaxction approvals and rejection
@login_required
@staff_required
@transaction.atomic
def approve_deposit(request, pk):

    deposit = get_object_or_404(
        Deposit,
        pk=pk,
        status='pending'
    )

    bank_account = deposit.user.bank_account

    # =========================
    # ADD BALANCE
    # =========================

    bank_account.balance += deposit.amount
    bank_account.save()

    # =========================
    # UPDATE DEPOSIT STATUS
    # =========================

    deposit.status = 'confirmed'
    deposit.save()

    # =========================
    # CREATE TRANSACTION HISTORY
    # =========================

    transaction = TransactionHistory.objects.create(

        user=deposit.user,

        amount=deposit.amount,

        transaction_type='deposit',

        direction='credit',

        description=(
            f"Approved {deposit.method} deposit"
        ),

        reference=generate_reference(),

        status="success",

        beneficiary_name="****self",

        beneficiary_number="******self",

        bank_name="First havin Bank",
    )

    # =========================
    # CREATE NOTIFICATION
    # =========================

    create_notification(

        user=deposit.user,

        title="Deposit Approved",

        message=(
            f"Your deposit of "
            f"{bank_account.get_currency_symbol()}"
            f"{deposit.amount} has been approved "
            f"successfully."
        ),

        notif_type="success",

        related_object=deposit
    )

    # =========================
    # EMAIL ALERT
    # =========================

    try:

        send_html_email(

            subject="Deposit Approved",

            to_email=deposit.user.email,

            template_name="emails/deposit_approved.html",

            context={

                'user': deposit.user,

                'amount': deposit.amount,

                'currency': (
                    bank_account.get_currency_symbol()
                ),

                'reference': transaction.reference,

                'dashboard_url': (
                    'https://www.firsthavinbk.com/'
                    'account/dashboard/'
                )
            }
        )

    except Exception as e:

        print(
            f"Deposit approval email failed: {e}"
        )

    messages.success(
        request,
        'Deposit approved successfully.'
    )

    return redirect(
        'staff:pending_transactions'
    )


@login_required
@staff_required
@transaction.atomic
def decline_deposit(request, pk):

    deposit = get_object_or_404(
        Deposit,
        pk=pk,
        status='pending'
    )

    deposit.status = 'failed'
    deposit.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=deposit.user,
        amount=deposit.amount,
        transaction_type='deposit',
        direction='credit',
        description=f"Declined {deposit.method} deposit",
        reference=generate_reference(),
        status="failed",

        beneficiary_name="****self",
        beneficiary_number="******self",
        bank_name="Dew Trust Bank",
    )

    # Notification
    create_notification(
        user=deposit.user,
        title="Deposit Declined",
        message=f"Your deposit of {deposit.user.bank_account.get_currency_symbol()}{deposit.amount} was declined.",
        notif_type="error",
        related_object=deposit
    )

    messages.warning(
        request,
        'Deposit declined.'
    )

    return redirect('staff:pending_transactions')


@login_required
@staff_required
@transaction.atomic
def approve_local_transfer(request, pk):

    transfer = get_object_or_404(
        LocalTransfer,
        pk=pk,
        status='pending'
    )

    # =========================
    # UPDATE STATUS
    # =========================

    transfer.status = 'successful'
    transfer.save()

    # =========================
    # CREATE TRANSACTION HISTORY
    # =========================

    transaction = TransactionHistory.objects.create(

        user=transfer.user,

        amount=transfer.amount,

        transaction_type='local_transfer',

        direction='debit',

        description=(
            f"Approved local transfer to "
            f"{transfer.beneficiary_name}"
        ),

        reference=generate_reference(),

        status="success",

        beneficiary_name=transfer.beneficiary_name,

        beneficiary_number=transfer.beneficiary_number,

        bank_name=transfer.bank_name,
    )

    # =========================
    # CREATE NOTIFICATION
    # =========================

    create_notification(

        user=transfer.user,

        title="Transfer Approved",

        message=(
            f"Your local transfer of "
            f"{transfer.user.bank_account.get_currency_symbol()}"
            f"{transfer.amount} was approved "
            f"successfully."
        ),

        notif_type="success",

        related_object=transfer
    )

    # =========================
    # EMAIL ALERT
    # =========================

    try:

        send_html_email(

            subject="Local Transfer Approved",

            to_email=transfer.user.email,

            template_name="emails/transfer_success.html",

            context={

                'user': transfer.user,

                'amount': transfer.amount,

                'currency': (
                    transfer.user.bank_account
                    .get_currency_symbol()
                ),

                'beneficiary': (
                    transfer.beneficiary_name
                ),

                'bank_name': transfer.bank_name,

                'reference': transaction.reference,

                'dashboard_url': (
                    'https://www.firsthavinbk.com/'
                    'account/dashboard/'
                )
            }
        )

    except Exception as e:

        print(
            f"Local transfer email failed: {e}"
        )

    messages.success(
        request,
        'Local transfer approved.'
    )

    return redirect(
        'staff:pending_transactions'
    )


@login_required
@staff_required
@transaction.atomic
def decline_local_transfer(request, pk):

    transfer = get_object_or_404(
        LocalTransfer,
        pk=pk,
        status='pending'
    )

    bank_account = transfer.user.bank_account

    # =========================
    # REFUND BALANCE
    # =========================

    bank_account.balance += transfer.amount
    bank_account.save()

    # =========================
    # UPDATE STATUS
    # =========================

    transfer.status = 'failed'
    transfer.save()

    # =========================
    # CREATE TRANSACTION HISTORY
    # =========================

    transaction = TransactionHistory.objects.create(

        user=transfer.user,

        amount=transfer.amount,

        transaction_type='local_transfer',

        direction='credit',

        description=(
            f"Refund for declined transfer "
            f"to {transfer.beneficiary_name}"
        ),

        reference=generate_reference(),

        status="failed",

        beneficiary_name=transfer.beneficiary_name,

        beneficiary_number=transfer.beneficiary_number,

        bank_name=transfer.bank_name,
    )

    # =========================
    # CREATE NOTIFICATION
    # =========================

    create_notification(

        user=transfer.user,

        title="Transfer Declined",

        message=(
            f"Your local transfer of "
            f"{bank_account.get_currency_symbol()}"
            f"{transfer.amount} was declined "
            f"and refunded."
        ),

        notif_type="error",

        related_object=transfer
    )

    # =========================
    # EMAIL ALERT
    # =========================

    try:

        send_html_email(

            subject="Local Transfer Declined",

            to_email=transfer.user.email,

            template_name="emails/transfer_declined.html",

            context={

                'user': transfer.user,

                'amount': transfer.amount,

                'currency': (
                    bank_account.get_currency_symbol()
                ),

                'beneficiary': (
                    transfer.beneficiary_name
                ),

                'bank_name': transfer.bank_name,

                'reference': transaction.reference,

                'dashboard_url': (
                    'https://www.firsthavinbk.com/'
                    'account/dashboard/'
                )
            }
        )

    except Exception as e:

        print(
            f"Declined transfer email failed: {e}"
        )

    messages.warning(
        request,
        'Local transfer declined and refunded.'
    )

    return redirect(
        'staff:pending_transactions'
    )


@login_required
@staff_required
@transaction.atomic
def approve_wire_transfer(request, pk):

    wire = get_object_or_404(
        InternationalTransfer,
        pk=pk,
        status='pending'
    )

    # =========================
    # UPDATE STATUS
    # =========================

    wire.status = 'successful'
    wire.save()

    # =========================
    # CREATE TRANSACTION HISTORY
    # =========================

    transaction = TransactionHistory.objects.create(

        user=wire.user,

        amount=wire.amount,

        transaction_type='wire_transfer',

        direction='debit',

        description=(
            f"Approved wire transfer to "
            f"{wire.beneficiary_name}"
        ),

        reference=generate_reference(),

        status="success",

        beneficiary_name=wire.beneficiary_name,

        beneficiary_number=wire.beneficiary_number,

        bank_name=wire.bank_name,
    )

    # =========================
    # CREATE NOTIFICATION
    # =========================

    create_notification(

        user=wire.user,

        title="Wire Transfer Approved",

        message=(
            f"Your wire transfer of "
            f"{wire.user.bank_account.get_currency_symbol()}"
            f"{wire.amount} was approved "
            f"successfully."
        ),

        notif_type="success",

        related_object=wire
    )

    # =========================
    # EMAIL ALERT
    # =========================

    try:

        send_html_email(

            subject="Wire Transfer Approved",

            to_email=wire.user.email,

            template_name="emails/transfer_success.html",

            context={

                'user': wire.user,

                'amount': wire.amount,

                'currency': (
                    wire.user.bank_account
                    .get_currency_symbol()
                ),

                'beneficiary': (
                    wire.beneficiary_name
                ),

                'bank_name': wire.bank_name,

                'reference': transaction.reference,

                'dashboard_url': (
                    'https://www.firsthavinbk.com/'
                    'account/dashboard/'
                )
            }
        )

    except Exception as e:

        print(
            f"Wire transfer email failed: {e}"
        )

    messages.success(
        request,
        'Wire transfer approved.'
    )

    return redirect(
        'staff:pending_transactions'
    )


@login_required
@staff_required
@transaction.atomic
def decline_wire_transfer(request, pk):

    wire = get_object_or_404(
        InternationalTransfer,
        pk=pk,
        status='pending'
    )

    bank_account = wire.user.bank_account

    # =========================
    # REFUND BALANCE
    # =========================

    bank_account.balance += wire.amount
    bank_account.save()

    # =========================
    # UPDATE STATUS
    # =========================

    wire.status = 'failed'
    wire.save()

    # =========================
    # CREATE TRANSACTION HISTORY
    # =========================

    transaction = TransactionHistory.objects.create(

        user=wire.user,

        amount=wire.amount,

        transaction_type='wire_transfer',

        direction='credit',

        description=(
            f"Refund for declined wire "
            f"transfer to {wire.beneficiary_name}"
        ),

        reference=generate_reference(),

        status="failed",

        beneficiary_name=wire.beneficiary_name,

        beneficiary_number=wire.beneficiary_number,

        bank_name=wire.bank_name,
    )

    # =========================
    # CREATE NOTIFICATION
    # =========================

    create_notification(

        user=wire.user,

        title="Wire Transfer Declined",

        message=(
            f"Your wire transfer of "
            f"{bank_account.get_currency_symbol()}"
            f"{wire.amount} was declined "
            f"and refunded."
        ),

        notif_type="error",

        related_object=wire
    )

    # =========================
    # EMAIL ALERT
    # =========================

    try:

        send_html_email(

            subject="Wire Transfer Declined",

            to_email=wire.user.email,

            template_name="emails/transfer_declined.html",

            context={

                'user': wire.user,

                'amount': wire.amount,

                'currency': (
                    bank_account.get_currency_symbol()
                ),

                'beneficiary': (
                    wire.beneficiary_name
                ),

                'bank_name': wire.bank_name,

                'reference': transaction.reference,

                'dashboard_url': (
                    'https://www.firsthavinbk.com/'
                    'account/dashboard/'
                )
            }
        )

    except Exception as e:

        print(
            f"Declined wire transfer email failed: {e}"
        )

    messages.warning(
        request,
        'Wire transfer declined and refunded.'
    )

    return redirect(
        'staff:pending_transactions'
    )


@login_required
@staff_required
def view_deposit_proof(request, pk):

    deposit = get_object_or_404(
        Deposit,
        pk=pk
    )

    context = {
        'deposit': deposit
    }

    return render(
        request,
        'staff/view_deposit_proof.html',
        context
    )


@login_required
@staff_required
def copy_transaction_history(request):

    form = CopyTransactionHistoryForm()

    if request.method == 'POST':

        form = CopyTransactionHistoryForm(request.POST)

        if form.is_valid():

            source_user = form.cleaned_data['source_user']
            target_user = form.cleaned_data['target_user']

            if source_user == target_user:

                messages.error(
                    request,
                    'Source and target users cannot be the same.'
                )

                return redirect(
                    'staff:copy_transaction_history'
                )

            transactions = TransactionHistory.objects.filter(
                user=source_user
            )

            copied_count = 0
            skipped_count = 0

            for tx in transactions:

                exists = TransactionHistory.objects.filter(
                    user=target_user,
                    copied_from=source_user,
                    amount=tx.amount,
                    created_at=tx.created_at,
                    description=tx.description,
                ).exists()

                if exists:

                    skipped_count += 1
                    continue

                TransactionHistory.objects.create(
                    user=target_user,
                    amount=tx.amount,
                    transaction_type=tx.transaction_type,
                    direction=tx.direction,
                    description=tx.description,
                    reference=generate_reference(),
                    status=tx.status,

                    beneficiary_name=tx.beneficiary_name,
                    beneficiary_number=tx.beneficiary_number,
                    bank_name=tx.bank_name,

                    created_at=tx.created_at,

                    copied_from=source_user
                )

                copied_count += 1

            messages.success(
                request,
                f'{copied_count} transactions copied successfully. '
                f'{skipped_count} duplicates skipped.'
            )

            return redirect(
                'staff:copy_transaction_history'
            )

    context = {
        'form': form
    }

    return render(
        request,
        'staff/copy_transaction_history.html',
        context
    )