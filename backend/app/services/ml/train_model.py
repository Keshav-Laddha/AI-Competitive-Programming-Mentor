from app.services.ml.solve_model import SolveProbabilityModel
from app.services.ml.training_dataset import build_training_dataset
from app.db.base import AsyncSessionLocal

async def train_solve_probability_model(topic_weakness_map, user_stats_map):
    async with AsyncSessionLocal() as db:
        X, y=await build_training_dataset(db, topic_weakness_map, user_stats_map)

    model=SolveProbabilityModel()
    model.train(X, y)

    return {
        "samples": len(y),
        "positive_rate": float(y.mean())
    }