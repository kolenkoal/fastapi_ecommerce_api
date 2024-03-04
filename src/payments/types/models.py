from sqlalchemy.orm import Mapped, relationship

from src.database import Base
from src.models import str256, uuidpk
from src.payments.methods.models import PaymentMethod  # noqa


class PaymentType(Base):
    __tablename__ = "payment_types"

    id: Mapped[uuidpk]
    name: Mapped[str256]

    payment_types_methods = relationship(
        "PaymentMethod", back_populates="payment_type"
    )
