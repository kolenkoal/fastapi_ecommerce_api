from sqlalchemy import insert, select

from src.database import async_session_factory
from src.utils.session import manage_session


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(
        cls,
        model_id,
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

    @classmethod
    async def find_all(cls):
        async with async_session_factory() as session:
            query = select(cls.model).order_by(cls.model.name)

            result = await session.execute(query)

            values = result.scalars().all()

            return values

    @classmethod
    async def validate_by_id(cls, value):
        async with async_session_factory() as session:
            query = select(cls.model).where(cls.model.id == value)

            result = (await session.execute(query)).scalar_one_or_none()

            return result

    @classmethod
    async def add(cls, **data):
        async with async_session_factory() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    @manage_session
    async def _create(cls, session=None, **data):
        create_query = insert(cls.model).values(**data).returning(cls.model)

        result = await session.execute(create_query)
        await session.commit()

        return result.scalar_one()
