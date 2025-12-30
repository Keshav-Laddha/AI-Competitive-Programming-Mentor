from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.db.schemas import MentorRequest, MentorResponse
from app.utils.auth import get_current_user
from app.services.mentor.mentor_engine import mentor_reply

router=APIRouter(prefix="/mentor", tags=["Mentor"])

@router.post("/chat", response_model=MentorResponse)
async def chat_with_mentor(payload: MentorRequest, db: AsyncSession=Depends(get_db), user=Depends(get_current_user)):

    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    reply=await mentor_reply(db=db, user_question=payload.question, problem_id=payload.problem_id)

    return MentorResponse(reply=reply)