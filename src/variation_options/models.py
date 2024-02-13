from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str256, uuidpk


class VariationOption(Base):
    __tablename__ = "variation_options"

    id: Mapped[uuidpk]
    value: Mapped[str256]
    variation_id: Mapped[UUID] = mapped_column(
        ForeignKey("variations.id", ondelete="CASCADE"), nullable=False
    )

    variation = relationship("Variation", back_populates="options")
