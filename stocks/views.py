import re
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string as rts
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
import secrets

from .models import *
from .stocks import checkStock
from .email import sendEmail

import threading


tickers = []

def index(request):
    return HttpResponse(rts("stocks/index.html", request=request))

def wait(request):
    if request.method == "POST":
        password = request.POST["password"]
        email = request.POST["email"]
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse(rts("stocks/emailInvalid.html", request=request))
        else:
            if Users.objects.filter(email=email).exists():
                user = Users.objects.get(email=email)
                if check_password(password, user.password):
                    request.session["loggedin"] = True
                    request.session["email"] = email
                    return HttpResponse(rts("stocks/in.html", request=request))
                else:
                    return HttpResponse(rts("stocks/emailTaken.html", request=request))
            else:
                theUser = Users.objects.create(email=email, password=make_password(password), confirmed=False)

                hashKey = secrets.token_hex(16)
                eamilConf = EmailConfirmations.objects.create(email=theUser,emailHash=hashKey) 
                verificationLink = request.get_host() + "/authorisation/" + str(hashKey)
                
                threading.Thread(target=sendEmail, args=(email, "yo", verificationLink)).start()

                return HttpResponse(rts("stocks/emailLink.html", request=request))
    else:
        return HttpResponse("hello")

def authorisation(request, authid):
    if EmailConfirmations.objects.filter(emailHash=authid):
        user = EmailConfirmations.objects.get(emailHash=authid)
        if user.email.confirmed == False:
            user.email.confirmed = True
            user.email.save()
            user.delete()
            return HttpResponse(rts("stocks/authorised.html", request=request))

    else:
        return HttpResponse(rts("stocks/emailOldLink.html", request=request))

def app(request):
    if "loggedin" in request.session:
        sessionEmail = request.session["email"]

        sessionUser = Users.objects.get(email=sessionEmail)
        tickers = sessionUser.stocks_set.all()

        notification = None;

        if request.method == "POST":
            post = request.POST
                
            if "tickerRemove" in post:
                ticker = post["tickerRemove"].upper()
                if tickers.filter(ticker=ticker):
                    tickerObject = tickers.get(ticker=ticker)
                    tickerObject.users.remove(sessionUser) 

            elif "tickerInput" in post:
                ticker = post["tickerInput"].upper()

                if 9 > len(ticker) > 0 and ticker.isalpha():
                    if not tickers.filter(ticker=ticker): 
                        if not Stocks.objects.filter(ticker=ticker): #checks if ticker doesn't exist in database
                            if checkStock(ticker):
                                t1 = Stocks(ticker=ticker)
                                t1.save()
                                t1.users.add(sessionUser)
                            else:
                                notification = "invalidTicker"

                        else: #exists in model
                            t1 = Stocks.objects.get(ticker=ticker)
                            t1.users.add(sessionUser)

                else:
                    notification = "invalidTicker"


        finalTickers = []

        for ticker in sessionUser.stocks_set.all():
            finalTickers.append(ticker.ticker) 

        return HttpResponse(rts("stocks/app.html", request=request, context={"tickers": finalTickers, "notification": notification}))
    else:
        return redirect("/enter/")
