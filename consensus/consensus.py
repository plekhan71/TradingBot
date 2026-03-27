# consensus/consensus.py

from consensus.strategy_weights import StrategyWeights

weights = StrategyWeights()


def consensus(
    results,
    min_strategies=2,
    min_confidence=1.2,
    htf_direction=None  # "UP" | "DOWN" | "FLAT" | None
):
    """
    results: list of tuples -> [(direction, confidence, name), ...]
    htf_direction: направление старшего ТФ (M15)

    return:
        signal: "UP" | "DOWN" | None
        confidence: float
        reason: str
    """

    if not results or not isinstance(results, list):
        return None, 0.0, "Нет результатов стратегий"

    ups = []
    downs = []

    for item in results:
        if not isinstance(item, (list, tuple)) or len(item) < 3:
            continue

        direction, confidence, name = item

        if direction not in ("UP", "DOWN"):
            continue

        if not isinstance(confidence, (int, float)) or confidence <= 0:
            continue

        # 🔥 динамические веса
        weight = weights.get(name)
        confidence *= weight

        if direction == "UP":
            ups.append((confidence, name))
        else:
            downs.append((confidence, name))

    if len(ups) < min_strategies and len(downs) < min_strategies:
        return None, 0.0, "Недостаточно подтверждений"

    up_conf = sum(c for c, _ in ups)
    down_conf = sum(c for c, _ in downs)

    # ⚔ конфликт направлений
    if len(ups) >= min_strategies and len(downs) >= min_strategies:
        if abs(up_conf - down_conf) < 0.3:
            return None, 0.0, "Конфликт стратегий"

    # 🧭 итоговое направление
    if len(ups) >= min_strategies and up_conf >= min_confidence and up_conf > down_conf:
        signal = "UP"
        confidence = up_conf
        reason = "UP подтверждён: " + ", ".join(f"{n}({c:.2f})" for c, n in ups)

    elif len(downs) >= min_strategies and down_conf >= min_confidence and down_conf > up_conf:
        signal = "DOWN"
        confidence = down_conf
        reason = "DOWN подтверждён: " + ", ".join(f"{n}({c:.2f})" for c, n in downs)

    else:
        return None, 0.0, "Сигнал слабый"

    # 🧱 HTF ФИЛЬТР (M15)
    if htf_direction:
        if htf_direction == "FLAT":
            return None, 0.0, "HTF FLAT — торговля запрещена"

        if signal != htf_direction:
            return None, 0.0, f"Против HTF ({htf_direction})"

    return signal, round(confidence, 2), reason
