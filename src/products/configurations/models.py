from uuid import UUID

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class ProductConfiguration(Base):
    __tablename__ = "configuration_product"

    product_item_id: Mapped[UUID] = mapped_column(
        GUID,
        ForeignKey("product_items.id", ondelete="CASCADE"),
        primary_key=True,
    )

    variation_option_id: Mapped[UUID] = mapped_column(
        GUID,
        ForeignKey("variation_options.id", ondelete="CASCADE"),
        primary_key=True,
    )
