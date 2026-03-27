import csv
import os

FILE = "data/trades.csv"

def log_trade(win):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([int(win)])

def total_trades():
    if not os.path.exists(FILE):
        return 0
    with open(FILE) as f:
        return sum(1 for _ in f)

def winrate():
    if not os.path.exists(FILE):
        return 0
    with open(FILE) as f:
        rows = [int(r.strip()) for r in f if r.strip()]
    return round(sum(rows) / len(rows) * 100, 2) if rows else 0
