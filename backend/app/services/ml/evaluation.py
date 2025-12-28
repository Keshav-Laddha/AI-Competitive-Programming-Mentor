import numpy as np
from sklearn.metrics import roc_auc_score, accuracy_score

def evaluate_model(model, X, y):
    probs=model.model.predict_proba(X)[:, 1]
    preds=(probs>=0.5).astype(int)

    return {
        "auc": roc_auc_score(y, probs),
        "accuracy": accuracy_score(y, preds),
        "avg_predicted_prob": float(probs.mean())
    }