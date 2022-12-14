import re
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string as rts
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
import secrets

from .stocks import checkStock
from .email import sendEmail
from .mongo import dbManager

dbm = dbManager(None)

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
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                if not dbm.emailExists(email):
                    hashKey = secrets.token_hex(16)
<<<<<<< HEAD
<<<<<<< HEAD
                    emailConf = EmailConfirmations.objects.create(email=user,emailHash=hashKey) 
=======
                    eamilConf = EmailConfirmations.objects.create(email=user,emailHash=hashKey) 
>>>>>>> parent of c300606 (trying db in pymongo (doesn't work))
=======
                    dbm.register(email, password, hashKey)

>>>>>>> parent of 91ad9b3 (Revert "trying db in pymongo (doesn't work)")
                    verificationLink = request.get_host() + "/authorisation/" + str(hashKey)
                    emailMessage = f"<html>To verify your account click the verification <a href='{verificationLink}'>link</a><br> {verificationLink}'</html>"
                    
                    print("shits sending")
                    threading.Thread(target=sendEmail, args=(email, "Stock Delta: Email Confirmation", emailMessage)).start()

                    #email being created
                    return HttpResponse(rts("stocks/emailLink.html", request=request))
                else:
                    #email regix fail register
                    notification = "Email taken"
            else:
                #email exists register
                notification = "Invalid email given"

        elif path == "login":
            if dbm.emailExists(email):
                if dbm.checkPassword(email, password):
                    request.session["loggedin"] = True
                    request.session["email"] = email
                    return redirect("/app/?loggedin=True")

            notification = "Invalid email or password"

    if request.GET.get("oldEmailLink", "False") == "True":
        notification = "Expired email link"

    return HttpResponse(rts("stocks/accountCreation.html", request=request, context={"notification": notification, "path": path}))
        

def authorisation(request, authid):
    email = dbm.confirmEmail(authid)
    print(email)
    if email:
        request.session["email"] = email
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

        tickers = dbm.getUserStocks(sessionEmail)

        #tickers = dbm.getUserStocks(email)

        if request.method == "POST":
            post = request.POST
                
            if "tickerRemove" in post:
                ticker = post["tickerRemove"].upper()
                if dbm.removeTickerFromUser(email, ticker):
                    tickers.remove(ticker)

            elif "tickerInput" in post:
                ticker = post["tickerInput"].upper()

                if 9 > len(ticker) > 0 and ticker.isalpha():
                    if not ticker in tickers: #checks ticker not already there
                        if not Stocks.objects.filter(ticker=ticker): #checks if ticker doesn't exist in database
                            if checkStock(ticker): #checks if valid
                                tickers.append(ticker)
                                dbm.addStock(email, ticker)
                            else:
                                notification = "invalidTicker"

                        else: #exists in model
                            tickers.append(ticker)
                            dbm.addStock(email, ticker)

                else:
                    notification = "invalidTicker"


        tickers.sort()

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
