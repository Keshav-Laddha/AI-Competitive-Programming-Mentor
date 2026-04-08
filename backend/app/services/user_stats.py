from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.models import Submission, Problem


async def get_user_stats(db: AsyncSession, user_id):

    # average difficulty of solved problems
    result = await db.execute(
        select(func.avg(Problem.difficulty))
        .join(Submission, Submission.problem_id == Problem.id)
        .where(
            Submission.user_id == user_id,
            Submission.verdict == "OK",
            Problem.difficulty.isnot(None)
        )
    )
    avg_difficulty = result.scalar() or 1200  # fallback only if no data


    # attempts on recent topics (approximation via last 50 submissions)
    recent = await db.execute(
        select(Problem.tags)
        .join(Submission, Submission.problem_id == Problem.id)
        .where(Submission.user_id == user_id)
        .order_by(Submission.created_at.desc())
        .limit(50)
    )

    topic_count = 0
    for row in recent.all():
        tags = row[0] or []
        topic_count += len(tags)

    attempts_on_topic = topic_count / 50 if topic_count else 0


    # recent accuracy (last 50 submissions)
    recent_subs = await db.execute(
        select(Submission.verdict)
        .where(Submission.user_id == user_id)
        .order_by(Submission.created_at.desc())
        .limit(50)
    )

    subs = recent_subs.scalars().all()
    if subs:
        correct = sum(1 for v in subs if v == "OK")
        recent_accuracy = correct / len(subs)
    else:
        recent_accuracy = 0.0


    return {
        "avg_difficulty": float(avg_difficulty),
        "attempts_on_topic": float(attempts_on_topic),
        "recent_accuracy": float(recent_accuracy)
    }