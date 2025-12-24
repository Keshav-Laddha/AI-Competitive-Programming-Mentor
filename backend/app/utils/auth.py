from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.base import get_db
from app.db.crud import get_user_by_id
from app.utils.security import decode_access_token

#OAuth2 Scheme
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str=Depends(oauth2_scheme), db: AsyncSession=Depends(get_db)):
    #Extracts user from JWT token.
    #Steps: decode JWT -> extract user_id -> fetch user from DB

    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    #decode token and extract user_id
    try:
        payload=decode_access_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    #fetch user
    user=await get_user_by_id(db, UUID(user_id))
    if user is None:
        raise credentials_exception

    #return user object
    return user