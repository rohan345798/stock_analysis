import mariadb
import sys


def ticker_exists(ticker: str, conn) -> int:
    sql = "select tickerid from tickers where ticker = ?;"
    cur = conn.cursor()
    cur.execute(sql, (ticker,))
    result = cur.fetchone()
    if result:
        return result[0]
    return 0


def enter_ticker(ticker: str, conn) -> int:
    ticker_id = ticker_exists(ticker, conn)
    if ticker_id == 0:
        sql = f"insert into tickers(ticker) values('{ticker}');"
        cur = conn.cursor()
        cur.execute(sql)
        print(f"{ticker} entered into db.")
    return ticker_exists(ticker, conn)

def date_exists(date: str, conn) -> int:
    sql = "select dateid from dates where datestring = ?;"
    cur = conn.cursor()
    cur.execute(sql, (date,))
    result = cur.fetchone()
    if result:
        return result[0]
    return 0


def enter_date(date: str, conn) -> int:
    date_id = date_exists(date, conn)
    if date_id == 0:
        sql = f"insert into dates(datestring) values('{date}');"
        cur = conn.cursor()
        cur.execute(sql)
        print(f"{date} entered into db.")
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
data_file = "/home/rohan/stock_analysis/INDEX_20210917.txt"
for line in open(data_file):
    line = line.strip()
    parts = line.split(",")
    ticker = parts[0]
    date = parts[1]
    print(f"ticker = {ticker} on {line}")
    print(enter_ticker(ticker, conn))
    print(f"date = {date} on {line}")
    print(enter_date(date, conn))
