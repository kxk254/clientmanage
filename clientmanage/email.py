from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView
from django.conf import settings
from email.mime.image import MIMEImage
import os

def send_client_email(subject, body, to, html_content=None, image_path=None, cc=None):
    """
    Send an email to the specified recipients.
    """
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to,
        cc=cc,
    )
    if html_content:
        email.attach_alternative(html_content, "text/html")
    
    if image_path:
        # Embed the image
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<embedded_image>')  # Use a unique ID
            img.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
            email.attach(img)  # Attach the image to the email

    email.send(fail_silently=False)


def send_test_email(subject, body, to, html_content=None, image_path=None, cc=None):
    """
    Send an email to the specified recipients.
    """
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to,
        cc=cc,
    )

    email.attach_alternative(html_content, "text/html")

    # Attach the inline image
    with open(image_path, "rb") as img_file:
        image = MIMEImage(img_file.read())
        image.add_header("Content-ID", "<embedded_image>")
        email.attach(image)

    # Send the email
    email.send()
    return JsonResponse({"message": "Test email sent successfully!"}, status=200)