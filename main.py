import time
from datetime import datetime

import MetaTrader5 as mt5

from telegram_bot import send
from mt5_data import get_candles
from strategies import run_strategies
from consensus.consensus import consensus
from filters.market_filter import MarketFilter
from trade_tracker import register_trade, check_trades, stats, strategy_stats

SYMBOL = "EURUSDrfd"
TIMEFRAME = "M1"
EXPIRATION_SECONDS = 180  # 3 минуты

# 🔒 ЗАЩИТЫ
COOLDOWN_SECONDS = 180
MAX_SAME_DIRECTION = 2

# 🧠 MARKET FILTER (M5)
market_filter = MarketFilter()


def log(msg):
    print(msg)
    send(msg)


def startup_check():
    report = []
    ok = True

    if not mt5.initialize():
        log("🔴 MT5 не запустился")
        return False

    report.append("✅ MT5 инициализирован")

    account = mt5.account_info()
    if account is None:
        report.append("❌ Аккаунт MT5 недоступен")
        ok = False
    else:
        report.append(f"✅ Аккаунт OK | Баланс: {account.balance:.2f} {account.currency}")

    info = mt5.symbol_info(SYMBOL)
    if info is None:
        report.append(f"❌ Символ {SYMBOL} не найден")
        ok = False
    else:
        if not info.visible:
            if not mt5.symbol_select(SYMBOL, True):
                report.append(f"❌ Не удалось активировать {SYMBOL}")
                ok = False
            else:
                report.append(f"✅ Символ {SYMBOL} активирован")
        else:
            report.append(f"✅ Символ {SYMBOL} доступен")

    tick = mt5.symbol_info_tick(SYMBOL)
    if tick is None or tick.bid == 0:
        report.append("❌ Нет тиков (цена не поступает)")
        ok = False
    else:
        report.append(f"✅ Цена есть | bid={tick.bid}")

    candles = get_candles(SYMBOL, TIMEFRAME, 100)
    if candles is None or len(candles) < 50:
        report.append("❌ Свечи не получены")
        ok = False
    else:
        report.append(f"✅ Свечи получены ({len(candles)})")

    log("🧪 Проверка системы:\n" + "\n".join(report))

    if not ok:
        log("⛔ БОТ ОСТАНОВЛЕН. Исправь ошибки и перезапусти.")
        mt5.shutdown()
        return False

    log("🚀 ВСЁ ГОТОВО. Бот начал работу.")
    return True


def main():
    log("🤖 MT5 Binary Bot запущен")

    if not startup_check():
        return

    last_signal_time = 0
    last_signal_direction = None
    same_direction_count = 0

    while True:
        # 🔹 M1 для входов
        candles = get_candles(SYMBOL, TIMEFRAME, 100)
        if candles is None:
            time.sleep(5)
            continue

        # 🔹 M5 для фильтра рынка
        candles_m5 = get_candles(SYMBOL, "M5", 100)
        if candles_m5 is None:
            time.sleep(5)
            continue

        # 🚫 ФЛЭТ → НЕ ТОРГУЕМ
        if market_filter.is_flat(candles_m5):
            time.sleep(5)
            continue

        results = run_strategies(candles)
        signal, confidence, reason = consensus(results, htf_direction=htf_trend)

        tick = mt5.symbol_info_tick(SYMBOL)
        if tick is None:
            time.sleep(5)
            continue

        now = time.time()

        # ⏳ cooldown
        if signal and now - last_signal_time < COOLDOWN_SECONDS:
            signal = None

        # 🔁 анти-серия
        if signal:
            if signal == last_signal_direction:
                if same_direction_count >= MAX_SAME_DIRECTION:
                    signal = None
                else:
                    same_direction_count += 1
            else:
                same_direction_count = 1
                last_signal_direction = signal

        if signal:
            price = tick.ask if signal == "UP" else tick.bid

            strategies_used = [
                name for direction, _, name in results if direction == signal
            ]

            msg = (
                f"📊 {SYMBOL}\n"
                f"{'📈 UP' if signal == 'UP' else '📉 DOWN'}\n"
                f"⏱ Таймфрейм: {TIMEFRAME}\n"
                f"⏳ Экспирация: 3 минуты\n"
                f"📍 Цена входа: {price}\n"
                f"🔥 Уверенность: {confidence:.2f}\n"
                f"🧠 Причина: {reason}\n"
                f"🧩 Стратегии: {', '.join(strategies_used)}\n"
                f"🕒 {datetime.now().strftime('%H:%M:%S')}"
            )

            log(msg)

            register_trade(signal, price, EXPIRATION_SECONDS, strategies_used)
            last_signal_time = now

        # 🔍 проверка сделок
        results_trades = check_trades(tick.bid)
        for r in results_trades:
            log(
                f"{r}\n"
                f"📊 Общая статистика:\n"
                f"WIN: {stats['win']} | LOSS: {stats['loss']}"
            )

            report = ["📊 Статистика стратегий:"]
            for name, s in strategy_stats.items():
                total = s["win"] + s["loss"]
                wr = (s["win"] / total * 100) if total > 0 else 0
                report.append(
                    f"{name}: {s['win']}W / {s['loss']}L | WR {wr:.1f}%"
                )

            log("\n".join(report))

        time.sleep(5)


if __name__ == "__main__":
    main()
