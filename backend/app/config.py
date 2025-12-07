#instead of hardcoding urls we store them in .env, and config.py is used to read those from .env safely
#Basesettings is a Pydantic class designed to load configuration values from .env
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str="redis://localhost:6379/0" #default value
    SECRET_KEY: str
    PGVECTOR_DIM: int=384 #embeddings are 384-dimensional (MiniLM model)
    OPENAI_API_KEY: str=None #optional

    class Config:
        env_file=".env" #load values from .env

settings=Settings()