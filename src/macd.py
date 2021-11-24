def calculate_sma(prices: list[float]):
    #simple moving avg needs to be calculated for 1st instance of ema, since ema is reccurring
    sum = 0
    #just avg of prices over time
    for i in prices:
        sum += i
    return sum/len(prices)

def calculate_ema(ema_yesterday:float, value:float, days:int):
    #2 is the smoothing value being used, is adjustable
    #calculate sma will be used for the first instance of this function being called
    ema = value*(2/(1+days))
    ema += (1-(2/(1+days)))
    return ema

def calculate_macd(ema_yesterday:float, value: float):

    return calculate_ema(value, 12) - calculate_ema(value, 26)

