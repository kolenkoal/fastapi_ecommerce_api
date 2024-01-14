from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models import str256, uuidpk


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[uuidpk]
    name: Mapped[str256] = mapped_column(unique=True)
