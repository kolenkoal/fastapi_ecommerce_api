import asyncio
import os
import sys

from sqlalchemy import select


current_file_path = os.path.abspath(__file__)

parent_dir = os.path.dirname(current_file_path)

grandparent_dir = os.path.dirname(parent_dir)

great_grandparent_dir = os.path.dirname(grandparent_dir)

sys.path.insert(1, os.path.dirname(grandparent_dir))

from src.config import settings  # noqa
from src.countries.models import Country  # noqa
from src.database import async_session_factory  # noqa
from src.payments.payment_types.models import PaymentType  # noqa
from src.users.models import Role, User  # noqa
from src.utils.data import payment_types_data  # noqa
from src.utils.data import admin_data, countries_data, roles_data  # noqa
from src.utils.hasher import Hasher  # noqa


async def insert_initial_values():
    async with async_session_factory() as session:
        query = select(Role).filter_by(name="user")

        result = await session.execute(query)

        role = result.all()

        if not role:
            for data in roles_data:
                role = Role(**data)
                session.add(role)

            await session.commit()

    async with async_session_factory() as session:
        hashed_password = Hasher.get_password_hash(
            admin_data["hashed_password"]
        )

        admin_data.update({"hashed_password": hashed_password})

        query = select(User).filter_by(email="admin@admin.com")

        result = await session.execute(query)

        admin = result.all()

        if not admin:
            admin = User(**admin_data)
            session.add(admin)

            await session.commit()

    async with async_session_factory() as session:
        query = select(Country)

        result = await session.execute(query)

        country = result.all()

        if not country:
            for data in countries_data:
                country = Country(**data)
                session.add(country)

            await session.commit()

    async with async_session_factory() as session:
        query = select(PaymentType)

        result = await session.execute(query)

        payment_types = result.all()

        if not payment_types:
            for data in payment_types_data:
                payment_type = PaymentType(**data)
                session.add(payment_type)

            await session.commit()


loop = asyncio.get_event_loop()
loop.run_until_complete(insert_initial_values())
