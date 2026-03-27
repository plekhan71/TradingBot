from .trend_ema import signal as trend_ema
from .breakout_range import signal as breakout_range
from .liquidity_grab import signal as liquidity_grab
from .momentum_atr import signal as momentum_atr

ALL_STRATEGIES = {
    "trend_ema": trend_ema,
    "breakout_range": breakout_range,
    "liquidity_grab": liquidity_grab,
    "momentum_atr": momentum_atr,
}


def run_strategies(candles):
    """
    Запускает все стратегии и собирает результаты
    Возвращает список:
    [
        ("UP"/"DOWN", confidence, strategy_name),
        ...
    ]
    """

    results = []

    for name, strategy in ALL_STRATEGIES.items():
        try:
            res = strategy(candles)

            # Стратегия молчит
            if res is None:
                continue

            # Ожидаем ("UP"/"DOWN", confidence)
            if not isinstance(res, (list, tuple)) or len(res) < 2:
                continue

            direction = res[0]
            confidence = res[1]

            if direction not in ("UP", "DOWN"):
                continue

            if not isinstance(confidence, (int, float)):
                continue

            if confidence <= 0:
                continue

            results.append((direction, float(confidence), name))

        except Exception as e:
            # Стратегия упала — бот живёт дальше
            print(f"⚠️ Стратегия {name} упала: {e}")

    return results
