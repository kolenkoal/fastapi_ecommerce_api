from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import uuidpk


class ShoppingCartItem(Base):
    __tablename__ = "shopping_cart_items"

    id: Mapped[uuidpk]
    cart_id: Mapped[UUID] = mapped_column(
        ForeignKey("shopping_carts.id", ondelete="CASCADE"), nullable=False
    )
    product_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("product_items.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(default=1)

    cart = relationship("ShoppingCart", back_populates="cart_items")
    item = relationship("ProductItem", back_populates="cart_items")
