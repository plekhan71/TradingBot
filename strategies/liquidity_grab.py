def signal(candles):
    prev = candles[-2]
    last = candles[-1]

    if last['low'] < prev['low'] and last['close'] > prev['low']:
        return "UP", 0.9

    if last['high'] > prev['high'] and last['close'] < prev['high']:
        return "DOWN", 0.9

    return None, 0
