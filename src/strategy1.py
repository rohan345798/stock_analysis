from loguru import logger
from datetime import date
from dataclasses import dataclass
import pandas_market_calendars as mcal
import math
from rsi import calculate_rsi
from stockdate import StockDate

# process the table in a way that gives us a list of tuples like [(ticker, [prices on the dates between 6/14/2001 and 6/28/2001])]
# use that to make a dictionary like {ticker, 14-day RSI}
from pricedatacache import get_price_data, get_stock_prices, get_all_tickers

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
    volume: int
    date: StockDate


class Portfolio:
    def __init__(self, initial_investment):
        self._cash = initial_investment
        self._ticker = None
        self._quantity = 0

    @property
    def has_value(self) -> bool:
        return self._cash > 0 or self._quantity > 0

    @property
    def ticker(self) -> str:
        return self._ticker

    def purchase(self, rsi_info: RsiData) -> None:
        if self._ticker:
            raise Exception(f"Cannot purchase because we already own {self._ticker}")
        self._ticker = rsi_info.ticker
        self._quantity = math.floor(self._cash / rsi_info.price)
        self._cash = self._cash - (self._quantity * rsi_info.price)

    def sell(self, rsi_info: RsiData) -> None:
        if self._ticker != rsi_info.ticker:
            raise Exception(
                f"Cannot sell {rsi_info.ticker} because portfolio has {self._ticker}"
            )
        self._cash += self._quantity * rsi_info.price
        self._quantity = 0
        self._ticker = None

    def __repr__(self):
        return f"Stock = {self._ticker}, Qty = {self._quantity}, Cash = {self._cash}"

    def get_value(self, rsi_info: RsiData) -> float:
        if self._ticker:
            if self._ticker != rsi_info.ticker:
                raise Exception(
                    f"Cannot value {rsi_info.ticker} because portfolio has {self._ticker}"
                )
            return self._cash + self._quantity * rsi_info.price
        else:
            return self._cash


def get_lowest_rsi_ticker(stock_date: StockDate) -> RsiData:
    """
    This method takes in a stock date and returns the ticker with the lowest rsi of that date.
    :param stock_date:
    :return:
    """
    last_15_days = get_last_15_days(stock_date)
    all_tickers = get_all_tickers()
    rsi_data_info = None
    for ticker in all_tickers:
        price_volumes = get_stock_prices(ticker, last_15_days)
        if any(price[0] == -1 for price in price_volumes):
            # logger.info(f"Ignored prices for {ticker}. prices = {prices}")
            continue
        this_rsi = calculate_rsi([price[0] for price in price_volumes])
        # logger.info(f"Calculated rsi = {this_rsi} for ticker = {ticker}, prices = {price_volumes}")
        if rsi_data_info is None or this_rsi < rsi_data_info.rsi:
            price, volume = get_price_data(ticker, stock_date.date)
            rsi_data_info = RsiData(ticker, this_rsi, price, volume, stock_date)
            start_stock_volume = sum([price[1] for price in price_volumes])
            logger.info(
                f"Updated --------------------- Current Lowest rsi = {rsi_data_info}"
            )
        elif this_rsi == rsi_data_info.rsi:
            # the rsi of this stock and the last stock are the same.
            # so calculate the volumes
            logger.info(f"Got ticker = {ticker} with same rsi Checking volumes.")
            new_stock_volume = sum([price[1] for price in price_volumes])
            if new_stock_volume >= rsi_data_info.volume:
                logger.info(
                    f"Old volume = {rsi_data_info.volume} smaller than {new_stock_volume}. Updating..."
                )
                price, volume = get_price_data(ticker, stock_date.date)
                rsi_data_info = RsiData(ticker, this_rsi, price, volume, stock_date)
                logger.info(
                    f"Added --------------------- Current Lowest rsi = {rsi_data_info}"
                )

    print(rsi_data_info)
    return rsi_data_info


def get_ticker_rsi(ticker: str, stock_date: StockDate) -> RsiData:
    last_15_days = get_last_15_days(stock_date)
    price_volumes = get_stock_prices(ticker, last_15_days)
    if any(price[0] == -1 for price in price_volumes):
        return None
    rsi = calculate_rsi([price[0] for price in price_volumes])
    price, volume = get_price_data(ticker, stock_date.date)
    return RsiData(ticker, rsi, price, volume, stock_date)


if __name__ == "__main__":
    start_date = StockDate(date(year=2001, month=6, day=28))
    current_date = StockDate(date(year=2001, month=6, day=28))
    last_date = StockDate(date(year=2021, month=6, day=28))
    portfolio = Portfolio(1000000)
    while portfolio.has_value and current_date.date < last_date.date:
        rsi_data = None
        if portfolio.ticker:
            # check if the rsi of the current held ticker
            # if it is over 70 sell.
            rsi_data = get_ticker_rsi(portfolio.ticker, current_date)
            if rsi_data and rsi_data.rsi >= 70:
                logger.info("------------------ Time to sell ---------------------")
                portfolio.sell(rsi_data)
        else:
            # if we do have any investment find the ticker with lowest RSI
            # and buy it
            rsi_data = get_lowest_rsi_ticker(current_date)
            portfolio.purchase(rsi_data)
        logger.info(
            f"Date = {current_date}, Portfolio = {portfolio}, value = {portfolio.get_value(rsi_data)}"
        )
        next_date = get_next_business_day(current_date)
        current_date = StockDate(date(next_date.year, next_date.month, next_date.day))
