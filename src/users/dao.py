from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import BaseDAO
from src.database import get_async_session
from src.users.models import Users


class UserDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_user_db(
        cls, session: AsyncSession = Depends(get_async_session)
    ):
        yield SQLAlchemyUserDatabase(session, Users)
