from pymongo import MongoClient
import pymongo
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

class dbManager():
    def __init__(self, period):


        client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        db = client["stocks"]

        #users: email, password, confirmed
        #emailConfirmation: email, emailHash
        #stocks: ticker, percentage
        #stocks-users: ticker, user

        self.users = db["users"]
        self.emailConfirmations = db["emailConfirmations"]
        self.stocks = db["stocks"]
        self.stocks_users = db["stocks_users"]

        #update stocks
        #iterate through each stock, check it exists in stock-users
        #update percentage

        self.period = period

    def deleteTickerNotInUse(self, ticker):
        query = {"ticker": ticker}
        if self.stocks_users.count_documents(query, limit = 1):
            return False
        else:
            self.stocks.delete_one(ticker)
            return True

    def updateTicker(self, ticker, percentage):
        query = {"ticker": ticker}
        update = {"$set": {"percentage": percentage}}

        self.stocks.update_one(query, update)

    #go through each user
    #get all their stocks in stock-users
    #email

    def getUserStocks(self, email):
        a = []
        for stock_user in self.stocks_users.find({"email": email}):
            ticker = stock_user.ticker

            stock = self.stocks.find_one({"ticker": ticker})
            a.append([ticker, stock.percentage])

        return a

    #register
    #check email doesn't exist already and is valid
    #create user record
    #create emailconf record

    def emailExists(self, email):
        if self.users.count_documents({"email": email}, limit = 1):
            return True
        return False

    def register(self, email, password, hashKey):
        self.users.insert_one({"email": email, "password": make_password(password), "confirmed": False})
        self.emailConfirmations.insert_one({"email": email, "emailHash": hashKey})

    def checkPassword(self, email, password):
        hashedPassword = self.users.find_one({"email": email}).password

        if check_password(password, hashedPassword):
            return True
        return False

    def confirmEmail(self, hashKey):
        result = self.emailConfirmations.find_one({"emailHash": hashKey})

        print("a", result)

        if result:
            email = result["email"]
            
            query = {"email": email}
            update = {"$set": {"confirmed": True}}

            self.users.update_one(query, update)

            self.emailConfirmations.delete_one({"email": email})

            return email
        return False
            
    def removeTickerFromUser(self, email, ticker):
        query = {"email": email, "ticker": ticker}
        if self.stocks_users.count_documents(query, limit=1) == 0:
            return False
        else:
            self.stocks_users.delete_one(query) 
            return True

    def addStock(self, email, ticker):
        self.stocks.insert_one({"ticker": ticker})
        self.stocks_users.insert_one({"ticker": ticker, "email": email})
#login
#check email exists
#check password

#authorisation
#confirm user email
#delete emailconfirmation record

#loggedin
#fetch all stocks of session user according to email

#ticker remove
#delete from stocks-users

#tickerinput
#check if ticker not already in ticker database
#then add to tickers
#add to stocks-users


