import time

# Активные сделки
active_trades = []

# Общая статистика
stats = {
    "win": 0,
    "loss": 0
}

# 📊 Статистика стратегий
# {
#   "trend_ema": {"win": 0, "loss": 0},
#   ...
# }
strategy_stats = {}


def register_trade(direction, price, expiration_seconds, strategies):
    """
    direction: "UP" | "DOWN"
    price: float
    expiration_seconds: int
    strategies: list[str] — стратегии, которые дали сигнал
    """
    active_trades.append({
        "direction": direction,
        "price": price,
        "expire_at": time.time() + expiration_seconds,
        "strategies": strategies
    })


def check_trades(current_price):
    """
    Проверяет истёкшие сделки,
    обновляет общую и стратегическую статистику
    """
    results = []

    for trade in active_trades[:]:
        if time.time() >= trade["expire_at"]:
            win = (
                current_price > trade["price"]
                if trade["direction"] == "UP"
                else current_price < trade["price"]
            )

            if win:
                stats["win"] += 1
                results.append("✅ WIN")
            else:
                stats["loss"] += 1
                results.append("❌ LOSS")

            # 📊 учёт стратегий
            for name in trade.get("strategies", []):
                strategy_stats.setdefault(name, {"win": 0, "loss": 0})
                if win:
                    strategy_stats[name]["win"] += 1
                else:
                    strategy_stats[name]["loss"] += 1

            active_trades.remove(trade)

    return results
