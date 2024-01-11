from sqlalchemy.orm import Mapped

from src.database import Base, str_256
from src.models import created_at, updated_at, uuidpk


class Users(Base):
    __tablename__ = "users"

    uuid: Mapped[uuidpk]
    email: Mapped[str_256]
    password: Mapped[str_256]
    first_name: Mapped[str_256]
    last_name: Mapped[str_256]
    phone_number: Mapped[str_256]
    created_at = Mapped[created_at]
    updated_at: Mapped[updated_at]
