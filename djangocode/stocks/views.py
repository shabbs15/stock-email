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

noReply = re.sub(".*@", "noreply@", os.environ["MAILGUN_SMTP_LOGIN"])



def index(request):
    template = loader.get_template('stocks/index.html')
    return HttpResponse(template.render(request=request))

def wait(request):
    if request.method == "POST":
        password = request.POST["password"]
        email = request.POST["email"]
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse("shit not valid")
        else:
            if User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists homenoy sorry")
            else:
                theUser = User.objects.create(email=email, password=make_password(password), confirmed=False)

                hashKey = secrets.token_hex(16)
                EmailConfirmation.objects.create(email=theUser,emailHash=hashKey) 
                verificationLink = request.get_host() + "/" + str(hashKey)
                
                send_mail(
                    subject="Email Confirmation",
                    message=verificationLink,
                    from_email=noReply,
                    recipient_list=[email],
                 )
                    
                return HttpResponse("pass")
    else:
        return HttpResponse("the fuck you trna do?")
