#!/usr/bin/env python3
from typing import List
from pathlib import Path
import mariadb
import sys
from datetime import datetime

ticker_cache = {}


def ticker_exists(ticker: str, conn) -> int:
    if ticker in ticker_cache:
        return ticker_cache[ticker]
    sql = "select tickerid from tickers where ticker = ?;"
    cur = conn.cursor()
    cur.execute(sql, (ticker,))
    result = cur.fetchone()
    if result:
        ticker_cache[ticker] = result[0]
        return result[0]
    return 0


def enter_ticker(ticker: str, conn) -> int:
    ticker_id = ticker_exists(ticker, conn)
    if ticker_id == 0:
        sql = f"insert into tickers(ticker) values('{ticker}');"
        cur = conn.cursor()
        cur.execute(sql)
    return ticker_exists(ticker, conn)


date_cache = {}


def date_exists(date: str, conn) -> int:
    if date in date_cache:
        return date_cache[date]
    sql = "select dateid from dates where datestring = ?;"
    cur = conn.cursor()
    cur.execute(sql, (date,))
    result = cur.fetchone()
    if result:
        date_cache[date] = result[0]
        return result[0]
    return 0


def enter_date(date: str, conn) -> int:
    date_id = date_exists(date, conn)
    if date_id == 0:
        sql = f"insert into dates(datestring) values('{date}');"
        cur = conn.cursor()
        cur.execute(sql)
    return date_exists(date, conn)


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

# Get Cursor

print("connection obtained.")


def price_data_exists(ticker_id: int, date_id: int, conn) -> bool:
    """
    Checks if a row exists in the database with this ticker_id and date_id
    :param ticker_id:
    :param date_id:
    :param conn:
    :return:
    """
    sql = "select * from pricedata where tickerid = ? and dateid = ?;"
    cur = conn.cursor()
    cur.execute(
        sql,
        (
            ticker_id,
            date_id,
        ),
    )
    result = cur.fetchone()
    return result


def delete_price_data(ticker_id: int, date_id: int, conn) -> None:
    sql = f"delete from pricedata where tickerid = ? and dateid = ?"
    cur = conn.cursor()
    cur.execute(
        sql,
        (
            ticker_id,
            date_id,
        ),
    )


def enter_price_data(ticker_id: int, date_id: int, parts: List[str], conn) -> int:
    """
    This method takes in the data about a single price information and enters it into the database.
    :param ticker_id:
    :param date_id:
    :param parts:
    :param conn:
    :return: The number of rows entered into the database
    """
    # check if this entry exists. If exists, delete and then enter
    if price_data_exists(ticker_id, date_id, conn):
        delete_price_data(ticker_id, date_id, conn)
    # do the data entry here
    sql = f"insert into pricedata(tickerid, dateid, openbid, openask, closebid, closeask, volume) values({ticker_id}, {date_id}, {parts[2]}, {parts[3]}, {parts[4]}, {parts[5]}, {parts[6]})"
    cur = conn.cursor()
    cur.execute(sql)


def load_file(filename: str) -> None:
    print(f"starting loading of file: {filename}")
    counter = 0
    for line in open(filename):
        line = line.strip()
        parts = line.split(",")
        ticker = parts[0]
        date = parts[1]
        ticker_id = enter_ticker(ticker, conn)
        formatted_date = datetime.strptime(date, "%d-%b-%Y").strftime("%Y%m%d")
        date_id = enter_date(formatted_date, conn)
        enter_price_data(ticker_id, date_id, parts, conn)
        counter += 1
        if counter % 100 == 0:
            print(counter)
    print(f"Completed loading of file: {filename}")


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 2:
        print(f"getting all files from path: {sys.argv[1]}")
        p = Path(sys.argv[1])
        for f in p.iterdir():
            if f.is_file():
                load_file(str(f))
