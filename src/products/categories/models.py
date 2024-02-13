from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str256
from src.products.models import Product  # noqa
from src.variations.models import Variation  # noqa


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str256]
    parent_category_id: Mapped[int] = mapped_column(
        ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=True
    )

    children_categories = relationship("ProductCategory", lazy="subquery")
    variations = relationship("Variation", back_populates="category")
    products = relationship("Product", back_populates="category")
