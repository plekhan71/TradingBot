from ml.model import train
from statistics import total_trades
from config import RETRAIN_AFTER_TRADES

_last = 0

def check():
    global _last
    if total_trades() - _last >= RETRAIN_AFTER_TRADES:
        train()
        _last = total_trades()
