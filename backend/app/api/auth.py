from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import UserCreate, UserLogin, UserOut, Token
from app.db.crud import get_user_by_email, create_user
from app.db.base import get_db
from app.utils.security import get_password_hash, verify_password, create_access_token

router=APIRouter(tags=["Auth"])

@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate, db: AsyncSession=Depends(get_db)):
    if await get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user=await create_user(db, email=payload.email, password_hash=get_password_hash(payload.password), display_name=payload.display_name)
    return user

@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db: AsyncSession=Depends(get_db)):
    user=await get_user_by_email(db, payload.email)

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token=create_access_token({"sub": str(user.id)})
    return {"access_token": token}