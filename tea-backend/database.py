import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
from sqlalchemy.ext.asyncio import AsyncSession
from contextvars import ContextVar

from log_state import db_counter


DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        try:
            token = db_counter.set(0)
            yield LoggingSession(session)
        finally:
            db_counter.reset(token)


class LoggingSession:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _increment(self):
        count = db_counter.get()
        db_counter.set(count + 1)

    def __getattr__(self, name):
        attr = getattr(self.session, name)
        if callable(attr) and name in ("execute", "scalars", "scalar", "get", "stream"):
            async def wrapper(*args, **kwargs):
                self._increment()
                return await attr(*args, **kwargs)
            return wrapper
        return attr