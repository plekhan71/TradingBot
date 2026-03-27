import pandas as pd
import joblib
from lightgbm import LGBMClassifier

DATA = "data/ml_dataset.csv"
MODEL = "data/model.pkl"

def train():
    df = pd.read_csv(DATA, header=None)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    model = LGBMClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.03
    )
    model.fit(X, y)
    joblib.dump(model, MODEL)
