from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str20, uuidpk
from src.products.items.utils import pick


class ProductItem(Base):
    __tablename__ = "product_items"

    id: Mapped[uuidpk]
    SKU: Mapped[str20] = mapped_column(default=pick(1))
    price: Mapped[Decimal] = mapped_column(nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(default=0)
    product_image: Mapped[str] = mapped_column(nullable=False)

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )

    product = relationship("Product", back_populates="product_items")
