from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Problem
from app.services.embeddings import embed_problem

async def embed_missing_problems(db: AsyncSession):
    result=await db.execute(select(Problem).where(Problem.embedding.is_(None)))

    problems=result.scalars().all()

    for problem in problems:
        problem.embedding=embed_problem(problem)

    await db.commit()