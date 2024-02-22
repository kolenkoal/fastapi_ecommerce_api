from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models import str20


class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, unique=False)
    status: Mapped[str20]
