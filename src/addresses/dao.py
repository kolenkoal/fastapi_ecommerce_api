from sqlalchemy import insert, select

from src.addresses.models import Address, UserAddress
from src.dao import BaseDAO
from src.database import async_session_factory


class AddressDAO(BaseDAO):
    model = Address

    @classmethod
    async def add(cls, user, **data):
        async with async_session_factory() as session:
            query = select(Address).filter_by(**data)
            address = await session.execute(query)
            if address:
                pass
                # Assign user_address user to

            query = select(UserAddress).where(UserAddress.user_id == user.id)

            user_addresses = await session.execute(query)

            if user_addresses:
                ...
                # insert and let

            # if not user_addresses:
            query = insert(cls.model).values(**data).returning(cls.model)
            new_address = await session.execute(query)
            await session.commit()

            return new_address.scalar()
