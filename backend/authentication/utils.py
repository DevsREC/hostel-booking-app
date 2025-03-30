from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

def send_email(subject, to_email, context):
    html_content = render_to_string('message.html', context)

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
