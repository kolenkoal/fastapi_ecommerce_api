from sqlalchemy import select

from src.countries.models import Country
from src.dao import BaseDAO
from src.database import async_session_factory


class CountryDAO(BaseDAO):
    model = Country

    @classmethod
    async def find_all(cls):
        async with async_session_factory() as session:
            query = select(cls.model).order_by(cls.model.name)

            result = await session.execute(query)

            countries = result.scalars().all()

            return countries

    @classmethod
    async def validate_country_by_id(cls, value):
        async with async_session_factory() as session:
            query = select(cls.model).where(cls.model.id == value)

            result = (await session.execute(query)).scalar()

            if not result:
                return False

            return True
