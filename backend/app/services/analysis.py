from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import TopicWeakness

async def get_user_weak_topics(db: AsyncSession, user_id):
    
    #returns the latest topic-wise weakness probabilities for a user.

    result=await db.execute(select(TopicWeakness.topic, TopicWeakness.weakness).where(TopicWeakness.user_id == user_id))

    rows=result.all()

    return {topic: weakness for topic, weakness in rows}