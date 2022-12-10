import requests
import os

from django.core.mail import send_mail

def sendEmail(email, subject, message):
    print("hi")
    send_mail(
        subject,
        "yo",
        "messages@stockpricedelta.xyz",
        [email],
        html_message=message,
        fail_silently = False
    )
    print("done")

