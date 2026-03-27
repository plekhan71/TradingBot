def signal(candles):
    bodies = [abs(c['close'] - c['open']) for c in candles[-5:]]
    avg = sum(bodies[:-1]) / 4
    last = bodies[-1]

    if last > avg * 1.8:
        direction = "UP" if candles[-1]['close'] > candles[-1]['open'] else "DOWN"
        return direction, 0.7

    return None, 0
