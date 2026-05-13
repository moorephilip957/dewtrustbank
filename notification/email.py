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

    if context is None:
        context = {}

    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    # Render HTML template
    html_content = render_to_string(template_name, context)

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body="This email requires HTML support.",
        from_email=from_email,
        to=[to_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()