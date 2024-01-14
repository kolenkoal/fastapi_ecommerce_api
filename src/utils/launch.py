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
from src.database import async_session_factory  # noqa
from src.users.models import Role, User  # noqa
from src.utils.hasher import Hasher  # noqa


async def insert_initial_values():
    async with async_session_factory() as session:
        query = select(Role).filter_by(name="user")

        result = await session.execute(query)

        role = result.scalar_one_or_none()

        if not role:
            roles_data = [
                {"name": "user"},
                {"name": "admin"},
                {"name": "manager"},
            ]

            for data in roles_data:
                role = Role(**data)
                session.add(role)

            await session.commit()

    async with async_session_factory() as session:
        admin_data = {
            "email": "admin@admin.com",
            "first_name": "Admin",
            "last_name": "Admin",
            "hashed_password": settings.ADMIN_PASSWORD,
            "role_id": 2,
        }

        hashed_password = Hasher.get_password_hash(
            admin_data["hashed_password"]
        )

        admin_data.update({"hashed_password": hashed_password})

        query = select(User).filter_by(email="admin@admin.com")

        result = await session.execute(query)

        admin = result.scalar_one_or_none()

        if not admin:
            admin = User(**admin_data)
            session.add(admin)

            await session.commit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert_initial_values())
