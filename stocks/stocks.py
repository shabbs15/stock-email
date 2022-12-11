import datetime
import time
import calendar
import finnhub
import os

fc = finnhub.Client(api_key=os.environ["FINNHUB_API_KEY"])

def checkStock(ticker):
    if fc.company_profile2(symbol=ticker):
        return True
    else:
        return False

class stockDataManager():
    def __init__(self):
        
        self.today = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
        self.endTimestamp = round(self.today.timestamp())

        if calendar.monthrange(self.today.year, self.today.month)[1] == self.today.day:
            self.period = "month"
            lastMonth = self.today.replace(day=1) - datetime.timedelta(days=1)
            self.timestamp = round(lastMonth.timestamp())

        elif self.today.weekday() == 4:
            self.period = "week"
            lastWeek = self.today - datetime.timedelta(days=7)
            self.timestamp = round(lastWeek.timestamp())

        else:
            dummyCandles = fc.stock_candles("AAPL", "D", self.endTimestamp - (60*60*24*40), self.endTimestamp)
            dummyTimestamp = dummyCandles["t"]
            if dummyTimestamp[-1] == self.endTimestamp:
                self.period = "day"
                yesterday = self.today - datetime.timedelta(days=1)
                self.timestamp = round(yesterday.timestamp())

            else:
                #self.period = "day"
                #yesterday = self.today - datetime.timedelta(days=1)
                #self.timestamp = round(yesterday.timestamp())

                self.period = None

    def updateDatabase(self,ticker):
        candles = fc.stock_candles(ticker, "D", self.endTimestamp - (60*60*24*40), self.endTimestamp) #gets data 40 days back
        timestampList = candles["t"]
        closeList = candles["c"]
        currentClose = closeList[-1]

        if self.period:

            stamp = self.timestamp

            count = 0

            while not stamp in timestampList or count == 5:
                stamp = stamp - (60*60*24)
                count += 1
            
            if stamp in timestampList:
                index = timestampList.index(stamp)
            
                price = closeList[index]


                return round((currentClose/price - 1) * 100,2)

        return None
