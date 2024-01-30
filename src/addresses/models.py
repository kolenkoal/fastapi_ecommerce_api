from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.countries.models import Country  # noqa
from src.database import Base
from src.models import str256, uuidpk


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[uuidpk]
    unit_number: Mapped[int] = mapped_column(nullable=False)
    street_number: Mapped[str256]
    address_line1: Mapped[str256]
    address_line2: Mapped[str256]
    city: Mapped[str256]
    region: Mapped[str256]
    postal_code: Mapped[str256]
    country_id: Mapped[uuidpk] = mapped_column(
        ForeignKey("countries.id", ondelete="CASCADE")
    )

    country = relationship("Country", back_populates="addresses")
