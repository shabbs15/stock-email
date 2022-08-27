import re
import os
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import make_password
import time
import secrets

from .models import User
from .models import EmailConfirmation

from django.core.mail import send_mail

from threading import Thread
import threading

noReply = re.sub(".*@", "noreply@", os.environ["MAILGUN_SMTP_LOGIN"])

def threadingSendMail(subject, message, from_email, recipientList):
    print("threading")
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipientList
    )
    print("threaded")


def index(request):
    template = loader.get_template('stocks/index.html')
    return HttpResponse(template.render(request=request))

def wait(request):
    if request.method == "POST":
        password = request.POST["password"]
        email = request.POST["email"]
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse("Email not valid")
        else:
            if User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists")
            else:
                theUser = User.objects.create(email=email, password=make_password(password), confirmed=False)

                hashKey = secrets.token_hex(16)
                EmailConfirmation.objects.create(email=theUser,emailHash=hashKey) 
                verificationLink = request.get_host() + "/" + str(hashKey)
                
                threading.Thread(target=threadingSendMail, args=("Email conf",
                    verificationLink,noReply,[email],)).start()

                return HttpResponse("pass")
    else:
        return HttpResponse("hello")
