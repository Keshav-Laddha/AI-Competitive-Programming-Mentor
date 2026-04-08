from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import ProblemOut
from app.db.crud import get_latest_recommendation
from app.db.base import get_db
from app.utils.auth import get_current_user
from app.db.models import Problem

router=APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/latest", response_model=list[ProblemOut] | None)
async def latest_recommendation(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # return await get_latest_recommendation(db, user.id)
    rec = await get_latest_recommendation(db, user.id)

    if not rec:
        return None

    problems = []
    for pid in rec.problems:
        p = await db.get(Problem, pid)
        if p:
            problems.append(p)

    return problems