from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import exc

from config import settings
import psycopg2

engine = create_engine(settings.database_url)
session_creater = sessionmaker(engine, class_ = Session, expire_on_commit = False)

class Base(DeclarativeBase):
    pass


def get_db():
    db = session_creater()
    try:
        yield db
    
    finally:
        db.close()
        

def create_db():
    try:
        return Base.metadata.create_all(engine)
    except exc.OperationalError:
        raise Exception('Невозможно подключиться к Базе данных. Проверьте, верные ли данные. Также проверьте, что вы запустили Docker контейнер')
        


# Async

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

async_engine = create_async_engine(settings.async_database_url)
async_session = sessionmaker(async_engine, class_ = AsyncSession, expire_on_commit = False)


# Redis
from redis import Redis
r = Redis(
    host = settings.REDIS_HOST,
    port = settings.REDIS_PORT,
    db = settings.REDIS_DB
)

