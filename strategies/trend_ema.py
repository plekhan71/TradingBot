import numpy as np

def signal(candles):
    close = np.array([c['close'] for c in candles])
    ema_fast = close[-5:].mean()
    ema_slow = close[-20:].mean()

    if ema_fast > ema_slow:
        return "UP", 0.8
    if ema_fast < ema_slow:
        return "DOWN", 0.8
    return None, 0
