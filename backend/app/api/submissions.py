from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import SubmissionOut
from app.db.crud import get_user_submissions
from app.db.base import get_db
from app.utils.auth import get_current_user

router=APIRouter(prefix="/submissions", tags=["Submissions"])

@router.get("/", response_model=list[SubmissionOut])
async def my_submissions(db: AsyncSession=Depends(get_db), user=Depends(get_current_user)):
    return await get_user_submissions(db, user.id)