def calculate_obv(volume: int, closing: float, prev_closing: float, obv: int) -> int:
    if closing > prev_closing:
        return obv+volume
    if closing == prev_closing:
        return obv
    if closing < prev_closing:
        return obv-volume
