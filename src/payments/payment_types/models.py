from sqlalchemy.orm import Mapped, relationship

from src.database import Base
from src.models import str256, uuidpk


class PaymentType(Base):
    __tablename__ = "payment_types"

    id: Mapped[uuidpk]
    name: Mapped[str256]

    payment_types_methods = relationship(
        "UserPaymentMethod", back_populates="payment_type"
    )
