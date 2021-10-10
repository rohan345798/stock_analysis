from datetime import date
from typing import Dict, Set, List, Tuple
import math
import mariadb
import sys
from dataclasses import dataclass

from data_load.data_loader import ticker_exists, date_exists, price_data_exists

PriceVolumeTuple = Tuple[float, int]

all_tickers_loaded = False
date_cache: Dict[date, int] = {}
ticker_cache: Dict[str, int] = {}
price_data_cache: Dict[int, Dict[int, PriceVolumeTuple]] = {}


# Connect to MariaDB Platform
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


def to_sql_date(d) -> str:
    return d.strftime("%Y%m%d")


def get_all_tickers() -> List[str]:
    global all_tickers_loaded
    if not all_tickers_loaded:
        sql = "select tickerid, ticker from tickers"
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        while result:
            ticker_cache[result[1]] = result[0]
            result = cur.fetchone()
        all_tickers_loaded = True
    return list(ticker_cache.keys())


def get_price_data(ticker, d) -> PriceVolumeTuple:
    if ticker not in ticker_cache:
        ticker_id = ticker_exists(ticker, conn)
        ticker_cache[ticker] = ticker_id
    ticker_id = ticker_cache[ticker]
    if d not in date_cache:
        date_id = date_exists(to_sql_date(d), conn)
        date_cache[d] = date_id
    date_id = date_cache[d]

    if ticker_id == 0 or date_id == 0:
        return -1, -1

    if ticker_id in price_data_cache and date_id in price_data_cache[ticker_id]:
        return price_data_cache[ticker_id][date_id]

    if ticker_id not in price_data_cache:
        price_data_cache[ticker_id] = {}
    if date_id not in price_data_cache[ticker_id]:
        result = price_data_exists(ticker_id, date_id, conn)
        if result:
            price_data_cache[ticker_id][date_id] = (round(result[4], 4), result[6])
        else:
            price_data_cache[ticker_id][date_id] = (-1, -1)
    return price_data_cache[ticker_id][date_id]


def get_stock_prices(ticker: str, dates: List[date]) -> List[PriceVolumeTuple]:
    ret_data: List[PriceVolumeTuple] = []
    for d in dates:
        ret_data.append(get_price_data(ticker, d))
    return ret_data


if __name__ == "__main__":
    get_stock_prices(
        "AXL",
    )
