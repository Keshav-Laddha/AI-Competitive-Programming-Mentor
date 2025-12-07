from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine=create_async_engine(settings.DATABASE_URL, future=True) #makes connection with database (basically connects python with any database PostgreSQL/MySQL/SQLite)
AsyncSessionLocal=sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) #to create sessions, (like create session connects with database do whatever required then closes once saved changes)
#expire-on_commit=false is used because SQLAlchemy clears the object in memory once committed so if needed again then we have to reload them again from the DB, so do not expire objects after commit keep them in memory and it will be freed from memory once session is closed
Base=declarative_base() #all db models inherit from Base, without it SQLAlchemy cannot track tables
async def get_db(): #integrates DB access into FastAPI route
    async with AsyncSessionLocal() as session:
        yield session #a session is created for every new API request and closes itself automatically