from twilio.rest import Client
from django.conf import settings


def send_sms_alert(user, message):

    try:

        if user.sms_alert != 'activate':
            return False

        phone = user.phone_number

        if not phone:
            return False

        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        # =========================
        # TRY ALPHANUMERIC SENDER
        # =========================

        try:

            sms = client.messages.create(

                body=message,

                from_=settings.TWILIO_SENDER_ID,

                to=phone
            )

            print(
                f"SMS sent using Sender ID "
                f"({sms.sid})"
            )

            return True

        except Exception as alpha_error:

            print(
                f"Sender ID failed: "
                f"{alpha_error}"
            )

            # =========================
            # FALLBACK TO NUMBER
            # =========================

            sms = client.messages.create(

                body=message,

                from_=settings.TWILIO_PHONE_NUMBER,

                to=phone
            )

            print(
                f"SMS sent using phone number "
                f"({sms.sid})"
            )

            return True

    except Exception as e:

        print(
            f"SMS sending failed: {e}"
        )

        return False
    

def send_transaction_sms(
    user,
    transaction_type,
    title,
    amount,
    currency,
    balance=None,
    reference=None,
    app_name="FirstHavin"
):
    icon = "DR" if transaction_type.upper() == "DEBIT" else "CR"
    message = (
        f"{app_name} ALERT\n"
        f"{title}\n"
        f"{icon} Amt: {currency}{amount:,.2f}\n"
    )

    if balance is not None:
        message += f"Bal: {currency}{balance:,.2f}\n"

    if reference:
        message += f"Ref: {reference}\n"

    message += "Thank you."

    return send_sms_alert(
        user=user,
        message=message
    )



# send_transaction_sms(
#     user=deposit.user,
#     title="Deposit Approved",
#     amount=deposit.amount,
#     currency=bank_account.get_currency_symbol(),
#     reference=transaction.reference
# )

# HAECO: A CR Amt $1900 has been posted to your account xxxxxx4427 successfully. 
# FRM: Thane P. xxxxxx1827 PMFB
# AMT will reflect in your account within 2 to 3 working days.