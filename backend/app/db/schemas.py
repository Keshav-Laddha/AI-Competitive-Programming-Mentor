from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime

#user schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str]=None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    display_name: Optional[str]
    created_at: datetime

    model_config=ConfigDict(from_attributes=True)

#cp_handle schemas
class CPHandleCreate(BaseModel):
    platform: str
    handle: str

class CPHandleOut(BaseModel):
    id: UUID
    platform: str
    handle: str
    metadata: Optional[dict]=None
    created_at: datetime
    last_synced: Optional[datetime]

    model_config=ConfigDict(from_attributes=True)

#problem schemas
class ProblemOut(BaseModel):
    id: UUID
    platform: str
    platform_problem_id: Optional[str]
    title: Optional[str]
    statement: Optional[str]
    tags: Optional[List[str]]
    difficulty: Optional[int]

    model_config=ConfigDict(from_attributes=True)

#submission schemas
class SubmissionOut(BaseModel):
    id: UUID
    platform_submission_id: Optional[str]
    verdict: Optional[str]
    language: Optional[str]
    time_taken_ms: Optional[int]
    memory: Optional[int]
    code: Optional[str]
    created_at: datetime

    problem_id: Optional[UUID]
    cp_handle_id: Optional[UUID]
    user_id: UUID

    model_config=ConfigDict(from_attributes=True)

#recommendation schemas
class RecommendationOut(BaseModel):
    id: UUID
    user_id: UUID
    name: Optional[str]
    problems: Optional[List[UUID]]
    created_at: datetime

    model_config=ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str="bearer"