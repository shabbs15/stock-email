import requests
import os

from django.core.mail import send_mail

def sendEmail(email, subject, message):
<<<<<<< HEAD
<<<<<<< HEAD
    print("meai")
=======
>>>>>>> parent of c300606 (trying db in pymongo (doesn't work))
=======
    print("hi")
>>>>>>> parent of 91ad9b3 (Revert "trying db in pymongo (doesn't work)")
    send_mail(
        subject,
        "yo",
        "messages@stockpricedelta.xyz",
        [email],
        html_message=message,
        fail_silently = False
<<<<<<< HEAD
<<<<<<< HEAD
    )
    print("mailed")

=======
)
>>>>>>> parent of c300606 (trying db in pymongo (doesn't work))
=======
    )
    print("done")

>>>>>>> parent of 91ad9b3 (Revert "trying db in pymongo (doesn't work)")
