def volatility_filter(candles):
    ranges = [c['high'] - c['low'] for c in candles[-10:]]
    return sum(ranges) / len(ranges) > 0.0003
