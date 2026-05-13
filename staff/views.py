from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.db.models import Sum, Count
from django.utils.timezone import now


from transaction.models import (
    Deposit,
    LocalTransfer,
    InternationalTransfer,
    TransactionHistory,
)
from .forms import (
    CustomerUpdateForm,
    BankAccountUpdateForm,
    AccountAdjustmentForm
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
from notification.email import send_html_email



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
            TransactionHistory.objects.create(
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
            TransactionHistory.objects.create(
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

    messages.success(request, 'KYC approved successfully.')

    return redirect('staff:kyc_requests')


@login_required
@staff_required
def reject_kyc(request, pk):

    kyc = get_object_or_404(KYCVerification, pk=pk)

    kyc.status = 'rejected'
    kyc.verified = False
    kyc.save()

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

            send_html_email(
                subject="New Support Response - Dew Trust Bank",
                to_email=ticket.user.email,
                template_name="emails/ticket_reply.html",
                context={
                    "user_name": ticket.user.username,
                    "ticket_reference": ticket.reference_id,
                    "message": message.content,
                    "ticket_url": f"https://firsthavinbk.com/tickets/{ticket.id}/",
                    "year": now().year
                }
            )

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

        title="Debit Card Approved",

        message=(
            "Your debit card has been approved "
            "and activated successfully."
        ),

        notif_type="success",

        related_object=card
    )

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
def customer_details(request, pk):

    customer = get_object_or_404(
        UserBankAccount.objects.select_related('user'),
        pk=pk
    )

    # Deposits
    deposits = Deposit.objects.filter(
        user=customer.user
    ).order_by('-created_at')

    # Local Transfers
    local_transfers = LocalTransfer.objects.filter(
        user=customer.user
    ).order_by('-created_at')

    # International Transfers
    wire_transfers = InternationalTransfer.objects.filter(
        user=customer.user
    ).order_by('-created_at')

    context = {
        'customer': customer,
        'deposits': deposits,
        'local_transfers': local_transfers,
        'wire_transfers': wire_transfers,
    }

    return render(
        request,
        'staff/customer_details.html',
        context
    )


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

    # Toggle Status
    if user.status == 'active':

        user.status = 'blocked'

        messages.warning(
            request,
            'Customer account has been blocked.'
        )

    else:

        user.status = 'active'

        messages.success(
            request,
            'Customer account has been activated.'
        )

    user.save()

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

    # Add Balance
    bank_account.balance += deposit.amount
    bank_account.save()

    # Update Deposit Status
    deposit.status = 'confirmed'
    deposit.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=deposit.user,
        amount=deposit.amount,
        transaction_type='deposit',
        direction='credit',
        description=f"Approved {deposit.method} deposit",
        reference=generate_reference(),
        status="success",

        beneficiary_name="****self",
        beneficiary_number="******self",
        bank_name="Dew Trust Bank",
    )

    # Notification
    create_notification(
        user=deposit.user,
        title="Deposit Approved",
        message=f"Your deposit of {bank_account.get_currency_symbol()}{deposit.amount} has been approved successfully.",
        notif_type="success",
        related_object=deposit
    )

    messages.success(
        request,
        'Deposit approved successfully.'
    )

    return redirect('staff:pending_transactions')


@login_required
@staff_required
@transaction.atomic
def decline_deposit(request, pk):

    deposit = get_object_or_404(
        Deposit,
        pk=pk,
        status='pending'
    )

    deposit.status = 'declined'
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

    transfer.status = 'successful'
    transfer.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=transfer.user,
        amount=transfer.amount,
        transaction_type='local_transfer',
        direction='debit',
        description=f"Approved local transfer to {transfer.beneficiary_name}",
        reference=generate_reference(),
        status="success",

        beneficiary_name=transfer.beneficiary_name,
        beneficiary_number=transfer.beneficiary_number,
        bank_name=transfer.bank_name,
    )

    # Notification
    create_notification(
        user=transfer.user,
        title="Transfer Approved",
        message=f"Your local transfer of {transfer.user.bank_account.get_currency_symbol()}{transfer.amount} was approved successfully.",
        notif_type="success",
        related_object=transfer
    )

    messages.success(
        request,
        'Local transfer approved.'
    )

    return redirect('staff:pending_transactions')


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

    # Refund Balance
    bank_account.balance += transfer.amount
    bank_account.save()

    # Update Status
    transfer.status = 'failed'
    transfer.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=transfer.user,
        amount=transfer.amount,
        transaction_type='local_transfer',
        direction='credit',
        description=f"Refund for declined transfer to {transfer.beneficiary_name}",
        reference=generate_reference(),
        status="failed",

        beneficiary_name=transfer.beneficiary_name,
        beneficiary_number=transfer.beneficiary_number,
        bank_name=transfer.bank_name,
    )

    # Notification
    create_notification(
        user=transfer.user,
        title="Transfer Declined",
        message=f"Your local transfer of {bank_account.get_currency_symbol()}{transfer.amount} was declined and refunded.",
        notif_type="error",
        related_object=transfer
    )

    messages.warning(
        request,
        'Local transfer declined and refunded.'
    )

    return redirect('staff:pending_transactions')


@login_required
@staff_required
@transaction.atomic
def approve_wire_transfer(request, pk):

    wire = get_object_or_404(
        InternationalTransfer,
        pk=pk,
        status='pending'
    )

    wire.status = 'successful'
    wire.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=wire.user,
        amount=wire.amount,
        transaction_type='wire_transfer',
        direction='debit',
        description=f"Approved wire transfer to {wire.beneficiary_name}",
        reference=generate_reference(),
        status="success",

        beneficiary_name=wire.beneficiary_name,
        beneficiary_number=wire.beneficiary_number,
        bank_name=wire.bank_name,
    )

    # Notification
    create_notification(
        user=wire.user,
        title="Wire Transfer Approved",
        message=f"Your wire transfer of {wire.user.bank_account.get_currency_symbol()}{wire.amount} was approved successfully.",
        notif_type="success",
        related_object=wire
    )

    messages.success(
        request,
        'Wire transfer approved.'
    )

    return redirect('staff:pending_transactions')


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

    # Refund
    bank_account.balance += wire.amount
    bank_account.save()

    # Update Status
    wire.status = 'failed'
    wire.save()

    # Transaction History
    TransactionHistory.objects.create(
        user=wire.user,
        amount=wire.amount,
        transaction_type='wire_transfer',
        direction='credit',
        description=f"Refund for declined wire transfer to {wire.beneficiary_name}",
        reference=generate_reference(),
        status="failed",

        beneficiary_name=wire.beneficiary_name,
        beneficiary_number=wire.beneficiary_number,
        bank_name=wire.bank_name,
    )

    # Notification
    create_notification(
        user=wire.user,
        title="Wire Transfer Declined",
        message=f"Your wire transfer of {bank_account.get_currency_symbol()}{wire.amount} was declined and refunded.",
        notif_type="error",
        related_object=wire
    )

    messages.warning(
        request,
        'Wire transfer declined and refunded.'
    )

    return redirect('staff:pending_transactions')


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