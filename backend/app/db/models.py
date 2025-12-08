from sqlalchemy import Column, String, Integer, Text, JSON, ARRAY, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY as PGARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
from pgvector.sqlalchemy import Vector
from app.config import settings
import uuid

#want users, cp_handles, problems, submissions, recommendations

class User(Base):
    __tablename__="users"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email=Column(String, unique=True, nullable=False)
    password_hash=Column(String, nullable=False)
    display_name=Column(String)
    created_at=Column(DateTime(timezone=True), server_default=func.now())

    #relationships
    cp_handles=relationship("CPHandle", back_populates="user")
    submissions=relationship("Submission", back_populates="user")
    recommendations=relationship("Recommendation", back_populates="user")

#user schema
#id email password name created_at

class CPHandle(Base):
    __tablename__="cp_handles"

    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    
    platform=Column(String, nullable=False)   #codeforces / codechef
    handle=Column(String, nullable=False)

    metadata=Column(JSON)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    last_synced=Column(DateTime(timezone=True))

    #relationships
    user=relationship("User", back_populates="cp_handles")
    submissions=relationship("Submission", back_populates="cp_handle")

class Problem(Base):
    __tablename__="problems"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform=Column(String, nullable=False)
    platform_problem_id=Column(String, unique=True)
    title=Column(String)
    statement=Column(Text)
    tags=Column(PGARRAY(String))
    difficulty=Column(Integer)
    embedding=Column(Vector(settings.PGVECTOR_DIM))
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())

    #relationships
    submissions=relationship("Submission", back_populates="problem")

class Submission(Base):
    __tablename__="submissions"

    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id=Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    cp_handle_id=Column(UUID(as_uuid=True), ForeignKey("cp_handles.id", ondelete="SET NULL"))
    problem_id=Column(UUID(as_uuid=True), ForeignKey("problems.id", ondelete="SET NULL"))

    platform_submission_id=Column(String)
    verdict=Column(String)
    language=Column(String)
    time_taken_ms=Column(Integer)
    memory=Column(Integer)
    code=Column(Text)

    created_at=Column(DateTime(timezone=True), server_default=func.now())

    #relationships
    user=relationship("User", back_populates="submissions")
    cp_handle=relationship("CPHandle", back_populates="submissions")
    problem=relationship("Problem", back_populates="submissions")


class Recommendation(Base):
    __tablename__="recommendations"

    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    name=Column(String) #eg daily-set-2025-02-01
    problems=Column(PGARRAY(UUID(as_uuid=True)))  #list of problem IDs
    created_at=Column(DateTime(timezone=True), server_default=func.now())

    #relationships
    user=relationship("User", back_populates="recommendations")


#relationships user<->cp handle, user<->submission, problem<->submission, user<->recommendations