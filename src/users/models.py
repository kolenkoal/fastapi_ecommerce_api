import uuid

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import GUID, UUID_ID
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models import created_at, str256, updated_at


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    id: Mapped[UUID_ID] = mapped_column(
        GUID, primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str256] = mapped_column(unique=True)
    hashed_password: Mapped[str256]
    first_name: Mapped[str256]
    last_name: Mapped[str256]
    phone_number: Mapped[str256] = mapped_column(unique=True)
    created_at = Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
