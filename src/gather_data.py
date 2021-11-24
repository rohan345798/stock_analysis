"""
With each sp500 ticker
we will gather the data from yfinance
Then for each day from 6/1/2001 to 6/1/2021 we will calculate three values
    - rsi
    - obv
    - macd
And store this data
"""
import csv
import yfinance as yf
import numpy as np
import pandas as pd
import mariadb
import sys

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


def calculate_obv(df):
    df["obv"] = np.where(
        df["Close"] > df["Close"].shift(1),
        df["Volume"],
        np.where(df["Close"] < df["Close"].shift(1), -df["Volume"], 0),
    ).cumsum()


def calculate_macd(df):
    exp1 = df[['Close']].ewm(span=12, adjust=False).mean()
    exp2 = df[['Close']].ewm(span=26, adjust=False).mean()
    exp3 = df[['Close']].ewm(span=9, adjust=False).mean()
    df["macd"] = exp1 - exp2
    df["macd_trend"] = exp3


def calculate_rsi(df):
    delta = df[['Close']].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up / ema_down
    df["rsi"] = 100 - (100/(1 + rs))


def sql_safe(data) -> str:
    if np.isnan(data):
        return "null"
    return str(data)


def save_to_db(hist, ticker):
    cur = conn.cursor()
    for index, row in hist.iterrows():
        sql = f"insert into all_data(datestring, ticker, open, high, low, close, volume, dividends, splits, \
         obv, macd, macd_trend, rsi) values('{index}', '{ticker}', {sql_safe(row['Open'])}, {sql_safe(row['High'])}, \
         {sql_safe(row['Low'])}, {sql_safe(row['Close'])}, {sql_safe(row['Volume'])}, {sql_safe(row['Dividends'])}, {sql_safe(row['Stock Splits'])}, \
        {sql_safe(row['obv'])}, {sql_safe(row['macd'])}, {sql_safe(row['macd_trend'])}, {sql_safe(row['rsi'])})"
        cur.execute(sql)


if __name__ == "__main__":
    with open("/home/rohan/stock_analysis/sp500.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ticker = row["Symbol"]
            print(f"Processing ticker = {ticker}")
            yf_data = yf.Ticker(ticker)
            hist = yf_data.history(period="max")
            calculate_obv(hist)
            calculate_macd(hist)
            calculate_rsi(hist)
            print("saving to db.")
            save_to_db(hist, ticker)

