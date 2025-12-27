import numpy as np
from app.services.ml.weakness_model import WeaknessModel

model=WeaknessModel()

def predict_topic_weakness(feature_map: dict):

    results={}

    for topic, features in feature_map.items():
        try:
            prob=model.predict_proba(features.reshape(1, -1))[0]
            results[topic]=round(float(prob), 3)
        except Exception:
            #fallback to heuristic normalization
            results[topic]=round(min(1.0, features[-1]/5), 3)  #weakness score scaled

    return results