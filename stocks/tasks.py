from .stocks import stockDataManager
from .models import Stocks, Users
from .email import sendEmail

from celery import shared_task


@shared_task(bind=True)
def massStockQuery(bro):
    stockList = Stocks.objects.all().distinct()
    
    sdm = stockDataManager()
    period = sdm.period

    print(period)

    if period:
        for stock in stockList:
            if stock.users.all(): # checks people actually want to have this stock and it's not just sitting in the database
                percentage = sdm.updateDatabase(stock.ticker)
                
                setattr(stock, "percentage", percentage)

                stock.save()
        
        userList = Users.objects.all().distinct()
        for user in userList:
            stocks = user.stocks_set.all()

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
                    ticker = stock.ticker
                    percentage = str(stock.percentage)
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
