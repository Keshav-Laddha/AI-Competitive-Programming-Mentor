from app.services.ml.solve_model import SolveProbabilityModel

model=SolveProbabilityModel()

def predict_solve_probability(features):
    try:
        return model.predict(features)
    except Exception:
        #return 0.5 #fallback in starting if no trainig dataset

        
        # fallback using difficulty gap (REAL logic, not random)
        difficulty = features[1]
        user_level = features[2]

        gap = difficulty - user_level

        if gap < -200:
            return 0.9
        elif gap < 0:
            return 0.7
        elif gap < 200:
            return 0.5
        elif gap < 400:
            return 0.3
        else:
            return 0.1