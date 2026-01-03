from fastapi import FastAPI
from app.api import auth, handles, submissions, recommendations, mentor, analysis, problems
from app.db.base import engine
from app.db.models import Base
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="CP Mentor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  #frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(handles.router)
app.include_router(submissions.router)
app.include_router(recommendations.router)
app.include_router(mentor.router)
app.include_router(analysis.router)
app.include_router(problems.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)