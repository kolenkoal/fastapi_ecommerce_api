from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str256, uuidpk
from src.variation_options.models import VariationOption  # noqa


class Variation(Base):
    __tablename__ = "variations"

    id: Mapped[uuidpk]
    name: Mapped[str256]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=False
    )

    category = relationship("ProductCategory", back_populates="variations")
    options = relationship("VariationOption", back_populates="variation")
