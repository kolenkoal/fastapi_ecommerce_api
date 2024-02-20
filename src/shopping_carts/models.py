from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import uuidpk
from src.shopping_carts.items.models import ShoppingCartItem  # noqa
from src.users.models import User  # noqa


class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    id: Mapped[uuidpk]

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="shopping_cart")

    # items: Mapped[list["ProductItem"]] = relationship(  # noqa
    #     back_populates="carts",
    #     secondary="shopping_cart_items",
    # )

    cart_items = relationship("ShoppingCartItem", back_populates="cart")
