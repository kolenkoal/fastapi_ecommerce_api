from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str256, uuidpk, uuidpk_not_unique


class UserPaymentMethod(Base):
    __tablename__ = "user_payment_methods"

    id: Mapped[uuidpk]
    user_id: Mapped[uuidpk_not_unique] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    payment_type_id: Mapped[uuidpk_not_unique] = mapped_column(
        ForeignKey("payment_types.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[str256]
    account_number: Mapped[str256]
    expiry_date: Mapped[date] = mapped_column(nullable=False)
    is_default: Mapped[bool] = mapped_column(default=True)

    payment_type = relationship(
        "PaymentType", back_populates="payment_types_methods"
    )

    user = relationship("User", back_populates="payment_methods")
