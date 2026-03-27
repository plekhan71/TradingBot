import joblib

MODEL = "data/model.pkl"
model = joblib.load(MODEL)

def predict(features):
    return model.predict_proba([features])[0][1]
