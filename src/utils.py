import pandas_market_calendars as mcal
from stockdate import StockDate

nyse = mcal.get_calendar("NYSE")


def get_last_15_days(stock_date: StockDate):
    early = nyse.schedule(
        start_date=stock_date.ago_days(30).yyyy_mm_dd, end_date=stock_date.yyyy_mm_dd
    )
    # early is the last 30 market days till the stock_date
    # so we reverse it, take 15 days of that and reverse is back
    # to return the market days in order for the last 15 days till stock_date
    return early["market_open"][::-1][:15][::-1]


def get_next_business_day(stock_date: StockDate):
    early = nyse.schedule(
        start_date=stock_date.days_forward(1).date,
        end_date=stock_date.days_forward(7).date,
    )
    return early["market_open"][0]
