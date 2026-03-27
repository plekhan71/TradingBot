import MetaTrader5 as mt5

def connect():
    if not mt5.initialize():
        return False, mt5.last_error()
    return True, None

def get_candles(symbol, timeframe, count=100):
    return mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
