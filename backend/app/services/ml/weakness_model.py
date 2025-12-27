import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from pathlib import Path

MODEL_PATH=Path("models/weakness_model.joblib")

class WeaknessModel:
    def __init__(self):
        self.model=LogisticRegression()
        self.is_trained=False

        if MODEL_PATH.exists():
            self.model=joblib.load(MODEL_PATH)
            self.is_trained=True

    def train(self, X: np.ndarray, y: np.ndarray):
        #X: shape (n_samples, n_features)
        #y: shape (n_samples,)
        self.model.fit(X, y)
        self.is_trained=True
        joblib.dump(self.model, MODEL_PATH)

    def predict_proba(self, X: np.ndarray)->np.ndarray:
        if not self.is_trained:
            raise RuntimeError("Model not trained")

        return self.model.predict_proba(X)[:, 1]