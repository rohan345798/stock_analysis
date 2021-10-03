from rsi import calculate_rsi

money = 1000000
#process the table in a way that gives us a list of tuples like [(ticker, [prices on the dates between 6/14/2001 and 6/28/2001])]
#use that to make a dictionary like {ticker, 14-day RSI}
ticker_rsi = {}
#find the ticker with the lowest RSI and buy as much as possible
#find the day that the RSI of said ticker goes above 70, and sell everything
#you can calculate how much money wouldve changed in this time by taking the price from the date when the RSI goes above 70 divided by the price from the date when the RSI went below 30 and multiplying the result by how much money was put in
#repeat until money<100 or date is 6/28/2021 (use while loop)


#if date == 6/28/2021:
#   print(money)