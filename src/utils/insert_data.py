import asyncio
import os
import sys

from sqlalchemy import select


current_file_path = os.path.abspath(__file__)

parent_dir = os.path.dirname(current_file_path)

grandparent_dir = os.path.dirname(parent_dir)

great_grandparent_dir = os.path.dirname(grandparent_dir)

sys.path.insert(1, os.path.dirname(grandparent_dir))

from src.database import async_session_factory  # noqa
from src.users.models import User  # noqa
from src.utils.hasher import Hasher  # noqa
from src.utils.other_data import user_data  # noqa


async def insert_dummy_data():
    async with async_session_factory() as session:
        query = select(User)

        users = (await session.execute(query)).all()

        print(len(users), users)

        if len(users) == 1:
            for data in user_data:
                hashed_password = Hasher.get_password_hash(
                    data["hashed_password"]
                )
                data.update({"hashed_password": hashed_password})
                print(data)
                user = User(**data)
                session.add(user)

                await session.commit()


loop = asyncio.get_event_loop()
loop.run_until_complete(insert_dummy_data())
