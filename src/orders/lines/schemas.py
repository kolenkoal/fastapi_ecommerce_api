from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class SOrderLineCreate(BaseModel):
    product_item_id: UUID
    order_id: UUID
    quantity: int
    price: Decimal


class SOrderLine(BaseModel):
    id: UUID
    product_item_id: UUID
    order_id: UUID
    quantity: int
    price: Decimal
