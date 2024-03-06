from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str256, uuidpk
from src.products.configurations.models import ProductConfiguration  # noqa
from src.variations.models import Variation  # noqa


class VariationOption(Base):
    __tablename__ = "variation_options"

    id: Mapped[uuidpk]
    value: Mapped[str256]
    variation_id: Mapped[UUID] = mapped_column(
        ForeignKey("variations.id", ondelete="CASCADE"), nullable=False
    )

    variation = relationship("Variation", back_populates="options")

    product_items: Mapped[list["ProductItem"]] = relationship(  # noqa
        back_populates="variations",
        secondary="configuration_product",
    )
