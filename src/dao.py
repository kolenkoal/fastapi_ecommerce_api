from uuid import UUID

from sqlalchemy import select

from src.database import async_session_factory


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(
        cls,
        model_id: UUID,
    ) -> model:
        async with async_session_factory() as session:
            query = select(cls.model).filter_by(id=model_id)

            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> model:
        async with async_session_factory() as session:
            query = select(cls.model).filter_by(**filter_by)

            result = await session.execute(query)

            return result.scalar_one_or_none()
