import csv
import os

FILE = "data/ml_dataset.csv"

def save(features, win):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(features + [int(win)])
