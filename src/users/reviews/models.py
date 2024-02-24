from typing import Literal
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str2000, uuidpk


RatingValues = Literal[1, 2, 3, 4, 5]


class UserReview(Base):
    __tablename__ = "user_reviews"

    id: Mapped[uuidpk]
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    ordered_product_id: Mapped[UUID] = mapped_column(
        ForeignKey("order_lines.id", ondelete="CASCADE"), nullable=False
    )
    rating_value: Mapped[int] = mapped_column(nullable=False)

    comment: Mapped[str2000] = mapped_column(nullable=True)

    user = relationship("User", back_populates="reviews")
    ordered_product = relationship("OrderLine", back_populates="reviews")

    __table_args__ = (
        CheckConstraint(
            "rating_value >= 1 and rating_value <= 5",
            name="check_rating_value_constraint",
        ),
    )
