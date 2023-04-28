from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_confirmation_link(to="", code=""):
    from_email = settings.EMAIL_HOST_USER
    to = [to]
    subject = "Confirm Your Email"
    context = {"code": code}
    content = render_to_string("mail/confirm_email.txt", context=context)
    email = EmailMessage(subject, content, from_email, to)
    response = email.send()
    return response
