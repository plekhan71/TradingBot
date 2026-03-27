from ml.predictor import predict
from config import ML_THRESHOLD

def allow(features):
    p = predict(features)
    return p >= ML_THRESHOLD, round(p, 3)
