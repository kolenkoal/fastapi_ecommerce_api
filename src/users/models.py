from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models import created_at, str256, updated_at, uuidpk


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    id: Mapped[uuidpk]
    email: Mapped[str256] = mapped_column(unique=True)
    hashed_password: Mapped[str256]
    first_name: Mapped[str256]
    last_name: Mapped[str256]
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
