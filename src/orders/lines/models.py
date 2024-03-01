from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import uuidpk
from src.users.reviews.models import UserReview  # noqa


class OrderLine(Base):
    __tablename__ = "order_lines"

    id: Mapped[uuidpk]
    product_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("product_items.id", ondelete="CASCADE"), nullable=False
    )
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("shop_orders.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[Decimal] = mapped_column(nullable=False)

    product_item = relationship(
        "ProductItem", back_populates="products_in_order"
    )
    order = relationship("ShopOrder", back_populates="products_in_order")
    reviews = relationship("UserReview", back_populates="ordered_product")
