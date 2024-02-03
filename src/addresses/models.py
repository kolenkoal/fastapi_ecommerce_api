from uuid import UUID

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.countries.models import Country  # noqa
from src.database import Base
from src.models import str256, uuidpk


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[uuidpk]
    unit_number: Mapped[str256]
    street_number: Mapped[str256]
    address_line1: Mapped[str256]
    address_line2: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str256]
    region: Mapped[str256]
    postal_code: Mapped[str256]
    country_id: Mapped[uuidpk] = mapped_column(
        ForeignKey("countries.id", ondelete="CASCADE")
    )

    country = relationship("Country", back_populates="addresses")

    users_living: Mapped[list["User"]] = relationship(  # noqa
        back_populates="addresses",
        secondary="user_addresses",
    )


class UserAddress(Base):
    __tablename__ = "user_addresses"

    user_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    address_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey("addresses.id", ondelete="CASCADE"), primary_key=True
    )

    is_default: Mapped[bool] = mapped_column(default=True)