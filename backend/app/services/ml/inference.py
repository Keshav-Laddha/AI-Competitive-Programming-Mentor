from app.services.ml.solve_model import SolveProbabilityModel

model=SolveProbabilityModel()

def predict_solve_probability(features):
    try:
        return model.predict(features)
    except Exception:
        return 0.5 #fallback in starting if no trainig dataset