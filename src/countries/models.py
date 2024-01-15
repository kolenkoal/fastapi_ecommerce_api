from sqlalchemy.orm import Mapped

from src.database import Base
from src.models import str256, uuidpk


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[uuidpk]
    name: Mapped[str256]
