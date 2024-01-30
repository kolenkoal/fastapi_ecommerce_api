from sqlalchemy import insert

from src.addresses.models import Address
from src.dao import BaseDAO
from src.database import async_session_factory


class AddressDAO(BaseDAO):
    model = Address

    @classmethod
    async def add(cls, **data):
        async with async_session_factory() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            new_address = await session.execute(query)
            await session.commit()

            return new_address.scalar()
