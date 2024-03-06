from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str256, uuidpk


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuidpk]
    name: Mapped[str256]
    description: Mapped[str]
    product_image: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=False
    )

    category = relationship("ProductCategory", back_populates="products")
    product_items = relationship("ProductItem", back_populates="product")
