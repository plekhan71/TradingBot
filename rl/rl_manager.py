from config import MAX_LOSSES_IN_ROW

_losses = 0

def allow():
    return _losses < MAX_LOSSES_IN_ROW

def record(win):
    global _losses
    _losses = 0 if win else _losses + 1
