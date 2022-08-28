import re
import os
from django.http import HttpResponse
from django.template.loader import render_to_string as rts
from django.contrib.auth.hashers import make_password
import time
import secrets

from .models import User
from .models import EmailConfirmation

import threading

import requests

myDomainName = os.environ["MAILGUN_DOMAIN"]
myApiKey = os.environ["MAILGUN_API_KEY"]

def sendMessageApi(email, subject, message):
    print("hello")
    files = [
        ('from', (None, f'Excited User <mailgun@{myDomainName}>')),
        ('to', (None, email)),
        ('subject', (None, subject)),
        ('text', (None, message)),
    ]

    response = requests.post(f'https://api.mailgun.net/v3/{myDomainName}/messages', files=files, auth=('api', myApiKey))
    print("done ")
        

def index(request):
    return HttpResponse(rts("stocks/index.html", request=request))

def wait(request):
    if request.method == "POST":
        password = request.POST["password"]
        email = request.POST["email"]
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse(rts("stocks/emailInvalid.html", request=request))
        else:
            if User.objects.filter(email=email).exists():
                return HttpResponse(rts("stocks/emailTaken.html", request=request))
            else:
                theUser = User.objects.create(email=email, password=make_password(password), confirmed=False)

                hashKey = secrets.token_hex(16)
                EmailConfirmation.objects.create(email=theUser,emailHash=hashKey) 
                verificationLink = request.get_host() + "/" + str(hashKey)
                
                threading.Thread(target=sendMessageApi, args=(email, "yo", verificationLink)).start()

                return HttpResponse(rts("stocks/emailLink.html", request=request))
    else:
        return HttpResponse("hello")
