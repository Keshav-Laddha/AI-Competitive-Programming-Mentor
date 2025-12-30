from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Problem, Submission
from app.services.ml.inference import predict_solve_probability
from app.services.ml.dataset_builder import build_training_sample
from app.services.novelty import compute_novelty
import numpy as np

min_target=0.55
max_target=0.75
recommendation_size=5

async def generate_ml_recommendations(db: AsyncSession, user_id, topic_weakness: dict, user_stats: dict):
    #fetch solved problems
    solved=await db.execute(select(Submission.problem_id).where(Submission.user_id==user_id, Submission.verdict=="OK"))
    solved_ids={r[0] for r in solved.all()}

    #fetch candidate problems
    result=await db.execute(select(Problem).where(Problem.difficulty.isnot(None)))
    problems=result.scalars().all()

    recommendations=[]

    recent = await db.execute(
        select(Problem.embedding)
        .join(Submission)
        .where(Submission.user_id == user_id)
        .order_by(Submission.created_at.desc())
        .limit(10)
    )

    recent_embeddings = [
        np.array(r[0]) for r in recent.all() if r[0] is not None
    ]


    for problem in problems:
        if problem.id in solved_ids:
            continue

        X, _=build_training_sample(topic_weakness, problem, user_stats, label=0)

        p_solve=predict_solve_probability(X)

        if min_target<=p_solve<=max_target:
            novelty=compute_novelty(np.array(problem.embedding), recent_embeddings)
            recommendations.append((problem, p_solve))

    #sort by closeness to ideal learning point
    recommendations.sort(
        key=lambda x:(
            abs(x[1]-0.65),  #learning zone closeness
            -x[2]  #higher novelty preferred
        )
    )

    return [p for p, _ in recommendations[:recommendation_size]]