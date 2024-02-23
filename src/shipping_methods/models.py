from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str256


class ShippingMethod(Base):
    __tablename__ = "shipping_methods"

    id: Mapped[int] = mapped_column(primary_key=True, unique=False)
    name: Mapped[str256]
    price: Mapped[Decimal] = mapped_column(nullable=False)

    orders = relationship("ShippingMethod", back_populates="shipping_method")
