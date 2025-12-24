from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.config import settings

#password hashing
#bcrypt is slow and secure so good against brute force
context=CryptContext(schemes=["bcrypt"], deprecated="auto")

#password utils
def get_password_hash(password: str) -> str:
    #hashes using bycrypt
    return context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    #verifies password entered by user with hashed_password
    return context.verify(plain_password, hashed_password)


#JWT tokens

def create_access_token(data: dict, expires_minutes: int=120) -> str:
    #data-> payload (usually {"sub": user_id})
    #exp-> expiry timestamp

    to_encode=data.copy()

    expire=datetime.now(datetime.timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    token=jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return token


def decode_access_token(token: str) -> dict:
    #to decode JWT tokens
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])