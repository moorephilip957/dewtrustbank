from notification.email import send_html_email
from notification.utils import create_notification
from notification.sms import send_transaction_sms


def handle_transaction_events(result, user, data, account):

    """
    Handles notifications and emails for:
    - success
    - pending
    - failed transactions
    """

    amount = data["amount"]
    beneficiary = data.get("beneficiary_name")
    bank_name = data.get("bank_name")

    # =========================
    # SUCCESS
    # =========================

    if result.status == "success":

        create_notification(

            user=user,

            title="Transfer Successful",

            message=(
                f"Your transfer of "
                f"{account.get_currency_symbol()}{amount} "
                f"was completed successfully."
            ),

            notif_type="success"
        )

        try:

            send_html_email(

                subject="Transfer Successful",

                to_email=user.email,

                template_name="emails/transfer_success.html",

                context={

                    "user": user,
                    "amount": amount,
                    "currency": account.get_currency_symbol(),
                    "beneficiary": beneficiary,
                    "bank_name": bank_name,
                    "reference": result.transaction.reference,
                    "dashboard_url": (
                        "https://www.firsthavinbk.com/account/dashboard/"
                    )
                }
            )

        except Exception as e:
            print(f"Success email error: {e}")

        send_transaction_sms(
            user=user,
            transaction_type="debit",
            title="Transfer Successful",
            amount=amount,
            balance=account.balance,
            currency=account.get_currency_symbol(),
            reference=result.transaction.reference
        )

    # =========================
    # PENDING
    # =========================

    elif result.status == "pending":

        create_notification(

            user=user,

            title="Transfer Pending",

            message=(
                f"Your transfer of "
                f"{account.get_currency_symbol()}{amount} "
                f"is pending approval."
            ),

            notif_type="info"
        )

        try:

            send_html_email(

                subject="Transfer Pending",

                to_email=user.email,

                template_name="emails/transfer_submitted.html",

                context={

                    "user": user,
                    "amount": amount,
                    "currency": account.get_currency_symbol(),
                    "beneficiary": beneficiary,
                    "bank_name": bank_name,
                    "dashboard_url": (
                        "https://www.firsthavinbk.com/account/dashboard/"
                    )
                }
            )

        except Exception as e:
            print(f"Pending email error: {e}")

        send_transaction_sms(
            user=user,
            transaction_type="debit",
            title="Transfer Pending",
            amount=amount,
            balance=account.balance,
            currency=account.get_currency_symbol(),
            reference=result.transaction.reference
        )

    # =========================
    # FAILED
    # =========================

    else:

        create_notification(

            user=user,

            title="Transfer Failed",

            message=(
                f"Your transfer of "
                f"{account.get_currency_symbol()}{amount} "
                f"failed."
            ),

            notif_type="error"
        )

        try:

            send_html_email(

                subject="Transfer Failed",

                to_email=user.email,

                template_name="emails/transfer_failed.html",

                context={

                    "user": user,
                    "amount": amount,
                    "currency": account.get_currency_symbol(),
                    "beneficiary": beneficiary,
                    "bank_name": bank_name,
                    "dashboard_url": (
                        "https://www.firsthavinbk.com/account/dashboard/"
                    )
                }
            )

        except Exception as e:
            print(f"Failed email error: {e}")

        send_transaction_sms(
            user=user,
            transaction_type="debit",
            title="Transfer Failed",
            amount=amount,
            balance=account.balance,
            currency=account.get_currency_symbol(),
            reference=result.transaction.reference
        )