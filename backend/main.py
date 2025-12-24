from fastapi import FastAPI
from app.api import auth, handles, submissions, recommendations

app = FastAPI(title="CP Mentor")

app.include_router(auth.router, prefix="/auth")
app.include_router(handles.router)
app.include_router(submissions.router)
app.include_router(recommendations.router)