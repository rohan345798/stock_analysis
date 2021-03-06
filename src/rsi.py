from typing import List

def calculate_rsi(prices: List[float]) -> float:
    average_gain = 0
    average_loss = 0

    for today, tomorrow in zip(
        prices, prices[1:]
    ):  # iterating two vars through prices one index apart
        if tomorrow > today:
            average_gain += tomorrow / today - 1  # percent calc
        else:
            average_loss += 1 - tomorrow / today  # percent calc

    if average_loss == 0:  # edge cases for if it never goes up or down
        if average_gain == 0:
            return 50.0
        else:
            return 100.0

    return 100 - (100 / (1 + average_gain / average_loss))  # formula
