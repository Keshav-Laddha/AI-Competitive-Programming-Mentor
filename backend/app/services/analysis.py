from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import TopicWeakness, Submission, Problem

# async def get_user_weak_topics(db: AsyncSession, user_id):
    
#     #returns the latest topic-wise weakness probabilities for a user.

#     result=await db.execute(select(TopicWeakness.topic, TopicWeakness.weakness).where(TopicWeakness.user_id == user_id))

#     rows=result.all()

#     return {topic: weakness for topic, weakness in rows}

async def get_user_weak_topics(db: AsyncSession, user_id):

    result = await db.execute(
        select(Submission, Problem)
        .join(Problem, Submission.problem_id == Problem.id)
        .where(Submission.user_id == user_id)
    )

    topic_stats = {}

    for submission, problem in result.all():
        for tag in problem.tags or []:
            if tag not in topic_stats:
                topic_stats[tag] = {"total": 0, "wrong": 0}

            topic_stats[tag]["total"] += 1

            if submission.verdict != "OK":
                topic_stats[tag]["wrong"] += 1

    # compute weakness
    weakness_map = {}

    for tag, stats in topic_stats.items():
        weakness = stats["wrong"] / stats["total"]
        weakness_map[tag] = round(weakness, 2)

        # store/update DB
        await db.merge(
            TopicWeakness(
                user_id=user_id,
                topic=tag,
                weakness=weakness
            )
        )

    await db.commit()

    return weakness_map