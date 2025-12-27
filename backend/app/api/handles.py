from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import CPHandleCreate, CPHandleOut
from app.db.crud import create_cp_handle, get_user_cp_handles
from app.db.base import get_db
from app.utils.auth import get_current_user
from rq import Queue
from redis import Redis
from app.workers.tasks import sync_codeforces_handle
from app.config import settings
from uuid import UUID
from app.db.models import CPHandle

router=APIRouter(prefix="/handles", tags=["CP Handles"])

@router.post("/", response_model=CPHandleOut)
async def add_handle(payload: CPHandleCreate, db: AsyncSession=Depends(get_db), user=Depends(get_current_user)):
    return await create_cp_handle(db, user_id=user.id, platform=payload.platform, handle=payload.handle)


@router.get("/", response_model=list[CPHandleOut])
async def list_handles(db: AsyncSession=Depends(get_db), user=Depends(get_current_user)):
    return await get_user_cp_handles(db, user.id)


redis_conn=Redis.from_url(settings.REDIS_URL)
queue=Queue("default", connection=redis_conn)

@router.post("/{handle_id}/sync")
async def sync_handle(handle_id: UUID, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    #fetch handle
    handle=await db.get(CPHandle, handle_id)

    if not handle or handle.user_id!=user.id:
        raise HTTPException(status_code=404, detail="Handle not found")

    #enqueue background sync
    queue.enqueue(sync_codeforces_handle, handle.id)

    return {
        "status": "sync_started",
        "handle_id": str(handle.id)
    }