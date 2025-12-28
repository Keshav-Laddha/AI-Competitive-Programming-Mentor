import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Submission, Problem
from app.services.ml.dataset_builder import build_training_sample

async def build_training_dataset(db: AsyncSession, topic_weakness_map: dict, user_stats_map: dict):

    X, y=[], []

    result=await db.execute(select(Submission, Problem).join(Problem, Submission.problem_id == Problem.id).where(Submission.verdict.isnot(None)))

    rows=result.all()

    for submission, problem in rows:
        label=1 if submission.verdict=="OK" else 0

        user_stats=user_stats_map.get(submission.user_id)
        if not user_stats:
            continue

        topic_weakness=topic_weakness_map.get(submission.user_id, {})
        features, target=build_training_sample(topic_weakness, problem=problem, user_stats=user_stats, label=label)

        X.append(features)
        y.append(target)

    return np.array(X), np.array(y)