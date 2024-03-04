from uuid import UUID

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    country_id: Mapped[UUID] = mapped_column(
        ForeignKey("countries.id", ondelete="CASCADE")
    )

    country = relationship("Country", back_populates="addresses")

    users_living: Mapped[list["User"]] = relationship(  # noqa
        back_populates="addresses",
        secondary="address_user",
    )

    orders = relationship("ShopOrder", back_populates="shipping_address")

    __mapper_args__ = {"eager_defaults": True}


class UserAddress(Base):
    __tablename__ = "address_user"

    user_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    address_id: Mapped[UUID] = mapped_column(
        GUID, ForeignKey("addresses.id", ondelete="CASCADE"), primary_key=True
    )

    is_default: Mapped[bool] = mapped_column(default=True)
