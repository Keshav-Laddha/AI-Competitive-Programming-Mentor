import joblib
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from pathlib import Path

MODEL_PATH=Path("models/solve_probability_model.joblib")
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

class SolveProbabilityModel:
    def __init__(self):
        self.model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
        ])
        self.trained = False

        if MODEL_PATH.exists():
            self.model=joblib.load(MODEL_PATH)
            self.trained=True

    def train(self, X: np.ndarray, y: np.ndarray):
        self.model.fit(X, y)
        self.trained=True
        joblib.dump(self.model, MODEL_PATH)

    def predict(self, X: np.ndarray) -> float:
        if not self.trained:
            raise RuntimeError("Model not trained")
        #return self.model.predict_proba(X.reshape(1, -1))[0][1]
        proba=self.model.predict_proba(X.reshape(1, -1))

        if proba.shape[1] == 1:
            return float(proba[0][0])
        
        return float(proba[0][1])