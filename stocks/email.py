import requests
import os

from django.core.mail import send_mail

def sendEmail(email, subject, message):
<<<<<<< HEAD
    print("meai")
=======
>>>>>>> parent of c300606 (trying db in pymongo (doesn't work))
    send_mail(
        subject,
        "yo",
        "messages@stockpricedelta.xyz",
        [email],
        html_message=message,
        fail_silently = False
<<<<<<< HEAD
    )
    print("mailed")

=======
)
>>>>>>> parent of c300606 (trying db in pymongo (doesn't work))
