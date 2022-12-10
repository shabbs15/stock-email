from .stocks import stockDataManager
from .models import Stocks, Users
from .email import sendEmail

from celery import shared_task
from mongo import dbManager


@shared_task(bind=True)
def massStockQuery(bro):
    sdm = stockDataManager()
    period = sdm.period

    dbm = dbManager(period)

    print(period)

    if period:
        for stock in dbm.stocks.find():
            ticker = stock.ticker
            if not dbm.deleteTickerNotInUse(ticker):
                #ticker exists
                percentage = sdm.updateDatabase(ticker)

                dbm.updateTicker(ticker, percentage)


        for user in dbm.users.find():
            email = user.email 

            stocks = dbm.getUserStocks(email=email)

            if len(stocks) > 0:
                htmlString = f"""<html>
                                    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="font-size: 25px">
                                        <tr>
                                            <td align="center">
                                                <table width="100%" cellspacing="0" cellpadding="0">
                                                    <tr style='background-color:aliceblue; text-align: center;'
                                                        <th style='text-align: center; width: 50%;'><b>Ticker</b></th>
                                                        <th style='text-align: center; width: 50%;'><b>{period.title()} Change</b></th>
                                                    </tr>
                                        """


                alternate = True
                for stock in stocks:
                    ticker = stock[0]
                    percentage = str(stock[1])
                    alternate = not alternate
                    if alternate:
                        htmlString += "<tr style='background-color:azure; text-align: center;'>"
                    else:
                        htmlString += "<tr style='text-align: center;'>"

                    htmlString += f"""
                                <td>{ticker}</td>
                                <td>{percentage}%</td>
                                </tr>
                                """


                htmlString += """</table>
                        </td>
                    </tr>
                </table>
                </html>
                """
                sendEmail(user.email, "Stock Update", htmlString)

    else:
        print("markets are closed")
