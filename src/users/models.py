from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.addresses.models import Address
from src.database import Base
from src.models import created_at, str256, updated_at, uuidpk


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str256] = mapped_column(unique=True)

    user = relationship("User", back_populates="role")


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    id: Mapped[uuidpk]
    email: Mapped[str256] = mapped_column(unique=True)
    hashed_password: Mapped[str256]
    first_name: Mapped[str256]
    last_name: Mapped[str256]
    created_at = Mapped[created_at]
    updated_at: Mapped[updated_at]
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        default=1,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    role = relationship("Role", back_populates="user")

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="users_living",
        secondary="user_addresses",
    )

    payment_methods = relationship("UserPaymentMethod", back_populates="user")
    shopping_cart = relationship("ShoppingCart", back_populates="user")
    orders = relationship("ShopOrder", back_populates="user")
    reviews = relationship("User", back_populates="user")
