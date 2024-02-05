from sqlalchemy.orm import Mapped

from src.database import Base
from src.models import str256, uuidpk


class PaymentType(Base):
    __tablename__ = "payment_types"

    id: Mapped[uuidpk]
    name: Mapped[str256]
