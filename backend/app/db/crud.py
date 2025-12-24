from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Optional, List
from uuid import UUID
from sqlalchemy import func

from app.db.models import (
    User,
    CPHandle,
    Problem,
    Submission,
    Recommendation
)


#User CRUD

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    res=await db.execute(select(User).where(User.email==email))
    return res.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
    res=await db.execute(select(User).where(User.id==user_id))
    return res.scalar_one_or_none()


async def create_user(db: AsyncSession, email: str, password_hash: str, display_name: Optional[str]) -> User:
    user=User(email=email, password_hash=password_hash, display_name=display_name) #created user entry
    db.add(user) #added to database
    await db.commit() #committed to database without committing does not reflect on database
    await db.refresh(user)
    return user


#CP_Handle CRUD

async def create_cp_handle(db: AsyncSession, user_id: UUID, platform: str, handle: str) -> CPHandle:
    cp_handle=CPHandle(user_id=user_id, platform=platform, handle=handle)
    db.add(cp_handle)
    await db.commit()
    await db.refresh(cp_handle)
    return cp_handle


async def get_user_cp_handles(db: AsyncSession, user_id: UUID) -> List[CPHandle]:
    res=await db.execute(select(CPHandle).where(CPHandle.user_id==user_id))
    return res.scalars().all()


async def update_handle_last_synced(db: AsyncSession, handle_id: UUID):
    await db.execute(update(CPHandle).where(CPHandle.id==handle_id).values(last_synced=func.now()))
    await db.commit()


#Problem CRUD

async def get_problem_by_platform_id(db: AsyncSession, platform: str, platform_problem_id: str) -> Optional[Problem]:
    res=await db.execute(select(Problem).where(Problem.platform==platform, Problem.platform_problem_id==platform_problem_id))
    return res.scalar_one_or_none()


async def create_problem(db: AsyncSession, **kwargs) -> Problem: 
    problem=Problem(**kwargs) #**kwargs because we don't know how many arguements we will get
    db.add(problem)
    await db.commit()
    await db.refresh(problem)
    return problem


async def get_problem_by_id(db: AsyncSession, problem_id: UUID) -> Optional[Problem]:
    res=await db.execute(select(Problem).where(Problem.id == problem_id))
    return res.scalar_one_or_none()


#Submission CRUD

async def create_submission(db: AsyncSession, **kwargs) -> Submission:
    submission=Submission(**kwargs)
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return submission


async def get_user_submissions(db: AsyncSession, user_id: UUID, limit: int=100)->List[Submission]:
    res=await db.execute(select(Submission).where(Submission.user_id==user_id).order_by(Submission.created_at.desc()).limit(limit))
    return res.scalars().all()


#Recommendation CRUD

async def create_recommendation(db: AsyncSession, user_id: UUID, name: str, problem_ids: List[UUID]) -> Recommendation:
    rec=Recommendation(user_id=user_id, name=name, problems=problem_ids)
    db.add(rec)
    await db.commit()
    await db.refresh(rec)
    return rec


async def get_latest_recommendation(
    db: AsyncSession, user_id: UUID) -> Optional[Recommendation]:
    res=await db.execute(select(Recommendation).where(Recommendation.user_id==user_id).order_by(Recommendation.created_at.desc()).limit(1))
    return res.scalar_one_or_none()