from typing import Annotated

from sqlalchemy import NullPool, String
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL_asyncpg
    DATABASE_PARAMS = {}

async_engine = create_async_engine(
    url=DATABASE_URL, echo=False, future=True, **DATABASE_PARAMS
)

async_session_factory = async_sessionmaker(
    async_engine, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


str_2000 = Annotated[str, 2000]
str_256 = Annotated[str, 256]
str_20 = Annotated[str, 20]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256), str_20: String(20)}
