from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import CPHandleCreate, CPHandleOut
from app.db.crud import create_cp_handle, get_user_cp_handles
from app.db.base import get_db
from app.utils.auth import get_current_user

router=APIRouter(prefix="/handles", tags=["CP Handles"])

@router.post("/", response_model=CPHandleOut)
async def add_handle(payload: CPHandleCreate, db: AsyncSession=Depends(get_db), user=Depends(get_current_user)):
    return await create_cp_handle(db, user_id=user.id, platform=payload.platform, handle=payload.handle)


@router.get("/", response_model=list[CPHandleOut])
async def list_handles(db: AsyncSession=Depends(get_db), user=Depends(get_current_user)):
    return await get_user_cp_handles(db, user.id)