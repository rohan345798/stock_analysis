from typing import Iterable

def calculate_rsi(prices: list[float]) -> float:
    gains = []
    losses = []
    for i in prices:
        if i > 0:
            gains.append(i)
        elif i < 0:
            losses.append(i*-1)

    avg_gain = 0
    avg_loss = 0
    for i in gains:
        avg_gain += i
    for i in losses:
        avg_loss += i
    avg_gain /= len(prices)
    avg_loss /= len(prices)

    if avg_loss == 0:
        if avg_gain == 0:
            return 50.0
        else:
            return 100.0
    else:
        return 100 - (100/(1+(avg_gain/avg_loss)))


