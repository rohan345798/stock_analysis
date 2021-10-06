from loguru import logger
from datetime import date
from dataclasses import dataclass
import pandas_market_calendars as mcal
from rsi import calculate_rsi
from stockdate import StockDate

# process the table in a way that gives us a list of tuples like [(ticker, [prices on the dates between 6/14/2001 and 6/28/2001])]
# use that to make a dictionary like {ticker, 14-day RSI}
from pricedatacache import get_price_data, get_stock_prices

ticker_rsi = {}
# find the ticker with the lowest RSI and buy as much as possible
# find the day that the RSI of said ticker goes above 70, and sell everything
# you can calculate how much money wouldve changed in this time by taking the price from the date when the RSI goes above 70 divided by the price from the date when the RSI went below 30 and multiplying the result by how much money was put in
# repeat until money<100 or date is 6/28/2021 (use while loop)


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


@dataclass
class RsiData:
    """
    This data class holds the data of the result of rsi calculation of a ticker for a date
    """

    ticker: str
    rsi: float
    price: float
    date: StockDate


@dataclass
class Portfolio:
    ticker: str
    qty: int


def get_lowest_rsi_ticker(stock_date: StockDate) -> RsiData:
    """
    This method takes in a stock date and returns the ticker with the lowest rsi of that date.
    :param stock_date:
    :return:
    """
    last_15_days = get_last_15_days(stock_date)
    prices = get_stock_prices("BBD", last_15_days)
    ticker_rsi = calculate_rsi(prices)
    print(ticker_rsi)


def purchase(rsi_data, current_investment) -> Portfolio:
    pass


def get_ticker_rsi(ticker) -> RsiData:
    pass


def sell(current_portfolio) -> float:
    pass


if __name__ == "__main__":
    start_date = StockDate(date(year=2001, month=6, day=28))
    current_date = StockDate(date(year=2001, month=6, day=28))
    last_date = StockDate(date(year=2021, month=6, day=28))
    initial_investment = 1000000.0
    current_investment = initial_investment
    current_portfolio = None
    ret_data = get_last_15_days(start_date)
    print(ret_data)
    while current_investment > 0 and current_date.date < last_date.date:
        if current_portfolio:
            # check if the rsi of the current held ticker
            # if it is over 70 sell.
            rsi_data = get_ticker_rsi(current_portfolio.ticker)
            if rsi_data.rsi >= 70:
                current_investment = sell(current_portfolio)
        else:
            # if we do have any investment find the ticker with lowest RSI
            # and buy it
            rsi_data = get_lowest_rsi_ticker(current_date)
            current_portfolio = purchase(rsi_data, current_investment)
        logger.info(f"Date = {current_date}, Portfolio = {current_portfolio}")
        next_date = get_next_business_day(current_date)
        current_date = StockDate(date(next_date.year, next_date.month, next_date.day))
