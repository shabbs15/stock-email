import requests
import os

myDomainName = os.environ["MAILGUN_DOMAIN"]
myApiKey = os.environ["MAILGUN_API_KEY"]
"""
def sendEmail(email, subject, message):
    files = [
        ('from', (None, f'Excited User <mailgun@{myDomainName}>')),
        ('to', (None, email)),
        ('subject', (None, subject)),
        ('html', (None, message))
    ]
    response = requests.post(f'https://api.mailgun.net/v3/{myDomainName}/messages', files=files, auth=('api', myApiKey))
"""

from django.core.mail import send_mail

def sendEmail(email, subject, message):
    send_mail(
        subject,
        message,
        "messages@stockpricedelta.xyz",
        [email],
        fail_silently = False
)
