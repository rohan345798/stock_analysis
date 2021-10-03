from datetime import date
from dataclasses import dataclass
import pandas_market_calendars as mcal
from rsi import calculate_rsi
from stockdate import StockDate
#process the table in a way that gives us a list of tuples like [(ticker, [prices on the dates between 6/14/2001 and 6/28/2001])]
#use that to make a dictionary like {ticker, 14-day RSI}
ticker_rsi = {}
#find the ticker with the lowest RSI and buy as much as possible
#find the day that the RSI of said ticker goes above 70, and sell everything
#you can calculate how much money wouldve changed in this time by taking the price from the date when the RSI goes above 70 divided by the price from the date when the RSI went below 30 and multiplying the result by how much money was put in
#repeat until money<100 or date is 6/28/2021 (use while loop)


nyse = mcal.get_calendar('NYSE')


def get_last_15_days(stock_date: StockDate):
    early = nyse.schedule(start_date=stock_date.ago_days(30).yyyy_mm_dd, end_date=stock_date.yyyy_mm_dd)
    # early is the last 30 market days till the stock_date
    # so we reverse it, take 15 days of that and reverse is back
    # to return the market days in order for the last 15 days till stock_date
    return early['market_open'][::-1][:15][::-1]


@dataclass
class RsiData:
    """
    This data class holds the data of the result of rsi calculation of a ticker for a date
    """
    ticker: str
    rsi: float
    price: float
    date: StockDate


def get_lowest_rsi_ticker(stock_date: StockDate) -> RsiData:
    """
    This method takes in a stock date and returns the ticker with the lowest rsi of that date.
    :param stock_date:
    :return:
    """
    last_15_days = get_last_15_days(stock_date)
    pass



if __name__ == "__main__":
    start_date = StockDate(date(year=2001, month=6, day=28))
    last_date = StockDate(date(year=2021, month=6, day=28))
    initial_investment = 1000000
    current_investment = initial_investment
    print(get_last_15_days(start_date))
    # if date == 6/28/2021:
    #   print(money)

