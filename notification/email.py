from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_html_email(
    subject,
    to_email,
    template_name,
    context=None,
    from_email=None
):

    context = context or {}

    from_email = (
        from_email or
        settings.DEFAULT_FROM_EMAIL
    )

    html_content = render_to_string(
        template_name,
        context
    )

    text_content = (
        "Please view this email in HTML format."
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to_email],
    )

    email.attach_alternative(
        html_content,
        "text/html"
    )

    email.send(fail_silently=False)



# send_html_email(
#     subject="Deposit Approved",
#     to_email=user.email,
#     template_name="emails/deposit_approved.html",
#     context={
#         'user': user,
#         'amount': deposit.amount,
#         'currency': user.bank_account.get_currency_symbol(),
#         'reference': transaction.reference,
#         'dashboard_url': 'https://www.firsthavinbk.com/account/dashboard/'
#     }
# )