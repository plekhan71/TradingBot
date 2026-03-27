def signal(candles):
    highs = [c['high'] for c in candles[-20:]]
    lows = [c['low'] for c in candles[-20:]]
    last = candles[-1]

    if last['close'] > max(highs[:-1]):
        return "UP", 0.75
    if last['close'] < min(lows[:-1]):
        return "DOWN", 0.75
    return None, 0
