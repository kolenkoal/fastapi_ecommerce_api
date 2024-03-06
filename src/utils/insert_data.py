import asyncio
import os
import sys

from sqlalchemy import select


current_file_path = os.path.abspath(__file__)

parent_dir = os.path.dirname(current_file_path)

grandparent_dir = os.path.dirname(parent_dir)

great_grandparent_dir = os.path.dirname(grandparent_dir)

sys.path.insert(1, os.path.dirname(grandparent_dir))

from src.auth.manager import UserManager, get_user_manager  # noqa
from src.database import async_session_factory  # noqa
from src.shopping_carts.router import create_shopping_cart  # noqa
from src.shopping_carts.schemas import SShoppingCartCreate  # noqa
from src.users.models import User  # noqa
from src.users.profiles.router import create_user_profile  # noqa
from src.users.schemas import UserCreate  # noqa
from src.utils.hasher import Hasher  # noqa
from src.utils.other_data import users_data  # noqa


async def insert_dummy_data():
    async with async_session_factory() as session:
        query = select(User)

        users = (await session.execute(query)).all()

        if len(users) == 1:
            for data in users_data:
                hashed_password = Hasher.get_password_hash(
                    data["hashed_password"]
                )
                data.update({"hashed_password": hashed_password})
                created_user = User(**data)
                session.add(created_user)

                await session.commit()

                shopping_cart_data = SShoppingCartCreate(
                    user_id=created_user.id
                )
                await create_shopping_cart(shopping_cart_data, created_user)

                await create_user_profile(created_user)


loop = asyncio.get_event_loop()
loop.run_until_complete(insert_dummy_data())
