from sqlalchemy import select

from src.dao import BaseDAO
from src.database import async_session_factory
from src.payments.types.models import PaymentType


class PaymentTypeDAO(BaseDAO):
    model = PaymentType

    @classmethod
    async def find_all(cls):
        async with async_session_factory() as session:
            query = select(cls.model).order_by(cls.model.name)

            result = await session.execute(query)

            payment_types = result.scalars().all()

            return payment_types
