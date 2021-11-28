"""

fixed amount in each stock upto a max of x%  (10 - 100 %)
purchase signal -> rsi < rsi_min , obv+ , macd over trendline
sell signal -> rsi > rsi_max and macd under trendline

"""
from dataclasses import dataclass
from stockdate import StockDate
from loguru import logger
from datetime import date
import mariadb
import sys
from typing import Dict, Set

from utils import get_next_business_day

INITIAL_INVESTMENT = 1000000.0
RSI_MIN = 30
RSI_MAX = 70
MAX_PERCENT_INVEST = .5
MIN_CASH_PERCENT = 0.05

try:
    conn = mariadb.connect(
        user="rohan",
        password="rohan",
        host="localhost",
        port=3306,
        database="stockdata",
    )
    conn.autocommit = True

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


class Portfolio:
    def __init__(self, initial_investment:float):
        self._cash = initial_investment
        self._holdings = {}

    @property
    def holdings(self) -> dict:
        return self._holdings

    def buy(self, ticker: str, amount: int, price: float):
        if ticker in self._holdings:
            raise Exception(f"{ticker} already in portfolio")

        if amount * price > self._cash:
            raise Exception(f"not enough cash to purchase.")

        self._holdings[ticker] = amount
        self._cash -= amount * price

    def sell(self, ticker: str, price: float):
        if ticker not in self._holdings:
            raise Exception(f"{ticker} not in portfolio")
        self._cash += self._holdings[ticker] * price
        del self._holdings[ticker]

    @property
    def has_value(self) -> bool:
        return self._cash > 0 or len(self._holdings) > 0

    @property
    def cash(self) -> float:
        return self._cash


@dataclass
class TickerData:
    open: float
    high: float
    low: float
    close: float
    volume: float
    dividends: float
    splits: float
    obv: float
    macd: float
    macd_trend: float
    rsi: float


def create_ticker_data(result):
    return TickerData(result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[11], result[12])


def get_day_data(current_date) -> Dict[str, TickerData]:
    cur = conn.cursor()
    tickers = {}
    sql = "select * from all_data where datestring='"+str(current_date)+" 00:00:00';"
    cur.execute(sql)
    result = cur.fetchone()
    while result:
        tickers[result[1]] = create_ticker_data(result)
        result = cur.fetchone()
    return tickers


def get_ticker_to_buy(data: Dict[str, TickerData], tickers: Set[str]) -> (str, float):
    potentials = []
    # get the potentials which are oversold and has a macd signal
    for t, t_data in data.items():
        if t not in purchased_tickers and t_data.rsi < RSI_MIN and t_data.macd_trend < t_data.macd:
            potentials.append((t, t_data.close, t_data.rsi))

    # if we did not find anything suitable return nothing
    if len(potentials) == 0:
        return None, None

    # we found only one suitable so return that
    if len(potentials) == 1:
        return potentials[0][0], potentials[0][1]

    # if there are more than one potential select the least rsi
    if len(potentials) > 1:
        return_ticker, return_price, return_rsi = potentials[0]
        for t, pr, rsi in potentials[1:]:
            if rsi < return_rsi:
                return_ticker, return_price, return_rsi = t, pr, rsi
        return return_ticker, return_price


if __name__ == "__main__":
    current_date = StockDate(date(year=2001, month=6, day=28))
    last_date = StockDate(date(year=2021, month=6, day=28))
    portfolio = Portfolio(INITIAL_INVESTMENT)
    while portfolio.has_value and current_date.date < last_date.date:
        day_data = get_day_data(current_date)

        # if we have more than the minimum level of cash then we buy something.
        purchased_tickers = set()
        purchased_tickers.update(portfolio.holdings.keys())
        while portfolio.cash > MIN_CASH_PERCENT * INITIAL_INVESTMENT:
            ticker, price = get_ticker_to_buy(day_data, purchased_tickers)
            if ticker is None:
                break
            cash_to_buy = min(portfolio.cash, INITIAL_INVESTMENT * MAX_PERCENT_INVEST)
            amount_to_buy = int(cash_to_buy/price)
            portfolio.buy(ticker, amount_to_buy, price)
            purchased_tickers.add(ticker)
            logger.info(f"{current_date} ------ Purchased ------ {ticker}, {amount_to_buy}, {price}.")

        next_date = get_next_business_day(current_date)
        current_date = StockDate(date(next_date.year, next_date.month, next_date.day))
