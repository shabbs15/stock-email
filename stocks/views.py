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
import json

tickers = []

def index(request):
    if "loggedin" in request.session:
        return redirect("/app/")
    else:
        return redirect("/register/")

def registerLogin(request):
    path = request.path.replace("/", "")
    notification = None

    if request.method == "POST":
        password = request.POST["password"]
        email = request.POST["email"]
        
        if path == "register":
            if not Users.objects.filter(email=email).exists():
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    user = Users.objects.create(email=email, password=make_password(password), confirmed=False)

                    hashKey = secrets.token_hex(16)
                    eamilConf = EmailConfirmations.objects.create(email=user,emailHash=hashKey) 
                    verificationLink = request.get_host() + "/authorisation/" + str(hashKey)
                    emailMessage = f"<html>To verify your account click the verification <a href='{verificationLink}'>link</a><br> {verificationLink}'</html>"
                    
                    threading.Thread(target=sendEmail, args=(email, "Stock Delta: Email Confirmation", emailMessage)).start()

                    #email being created
                    return HttpResponse(rts("stocks/emailLink.html", request=request))
                else:
                    #email regix fail register
                    notification = "Invalid email given"
            else:
                #email exists register
                notification = "Email taken"

        elif path == "login":
            if Users.objects.filter(email=email).exists():
                user = Users.objects.get(email = email)

                if check_password(password, user.password):
                    request.session["loggedin"] = True
                    request.session["email"] = email
                    return redirect("/app/?loggedin=True")

            notification = "Invalid email or password"

    if request.GET.get("oldEmailLink", "False") == "True":
        notification = "Expired email link"

    return HttpResponse(rts("stocks/accountCreation.html", request=request, context={"notification": notification, "path": path}))
        

def authorisation(request, authid):
    if EmailConfirmations.objects.filter(emailHash=authid):
        user = EmailConfirmations.objects.get(emailHash=authid)
        if user.email.confirmed == False:
            user.email.confirmed = True
            user.email.save()
            user.delete()

            request.session["email"] = user.email.email
            request.session["loggedin"] = True
            return redirect("/app/?verified=True")
    else:
        return redirect("/register/?oldEmailLink=True")

def app(request):
    if "loggedin" in request.session:
        notification = None;

        if request.GET.get("verified", "False") == "True":
            notification = "verified"
        elif request.GET.get("loggedin", "False") == "True":
            notification = "loggedin"

        sessionEmail = request.session["email"]

        sessionUser = Users.objects.get(email=sessionEmail)
        tickers = sessionUser.stocks_set.all()

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

        finalTickers.sort()

        return HttpResponse(rts("stocks/app.html", request=request, context={"tickers": finalTickers, "notification": notification}))
    else:
        return redirect("/login/")

def pageNotFound(request, exception):
    return HttpResponse(rts("stocks/404.html", request=request))

def logout(request):
    if "email" in request.session:   
        del request.session["email"]
    if "loggedin" in request.session:
        del request.session["loggedin"]

    return redirect("/login/")
