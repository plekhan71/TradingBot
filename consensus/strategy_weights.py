# consensus/strategy_weights.py

from trade_tracker import strategy_stats


class StrategyWeights:
    def __init__(self):
        self.min_trades = 5  # пока мало сделок — не делаем резких выводов
        self.default_weight = 1.0
        self.min_weight = 0.6
        self.max_weight = 1.4

    def get(self, name: str) -> float:
        stats = strategy_stats.get(name)

        if not stats:
            return self.default_weight

        wins = stats.get("win", 0)
        losses = stats.get("loss", 0)
        total = wins + losses

        if total < self.min_trades:
            return self.default_weight

        wr = wins / total * 100

        if wr < 40:
            return 0.6
        elif wr < 55:
            return 0.8
        elif wr < 65:
            return 1.0
        elif wr < 75:
            return 1.2
        else:
            return 1.4
