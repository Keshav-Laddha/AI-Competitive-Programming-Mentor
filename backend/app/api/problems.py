from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.base import get_db
from app.db.schemas import ProblemOut
from app.db.crud import get_problem_by_id
from app.utils.auth import get_current_user

router=APIRouter(prefix="/problems", tags=["Problems"])


@router.get("/{problem_id}", response_model=ProblemOut)
async def get_problem(problem_id: UUID, db: AsyncSession=Depends(get_db), user=Depends(get_current_user)):

    problem=await get_problem_by_id(db, problem_id)

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    return problem