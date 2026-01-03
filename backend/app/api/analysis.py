from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.utils.auth import get_current_user
from app.services.analysis import get_user_weak_topics

router=APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/weak-topics")
async def weak_topics(db: AsyncSession=Depends(get_db), user=Depends(get_current_user)):
    return await get_user_weak_topics(db, user.id)