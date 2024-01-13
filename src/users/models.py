from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models import created_at, str256, updated_at, uuidpk


class Users(Base):
    __tablename__ = "users"

    uuid: Mapped[uuidpk]
    email: Mapped[str256] = mapped_column(unique=True)
    password: Mapped[str256]
    first_name: Mapped[str256]
    last_name: Mapped[str256]
    phone_number: Mapped[str256] = mapped_column(unique=True)
    created_at = Mapped[created_at]
    updated_at: Mapped[updated_at]
