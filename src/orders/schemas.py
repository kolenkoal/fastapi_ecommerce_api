from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.orders.lines.schemas import SOrderLineWithoutOrder


class SOrderCreate(BaseModel):
    payment_method_id: UUID
    shipping_address_id: UUID
    shipping_method_id: int


class SOrderChangeOptional(BaseModel):
    order_status_id: Optional[int] = None


class SOrder(BaseModel):
    id: UUID
    user_id: UUID
    order_date: date
    payment_method_id: UUID
    shipping_address_id: UUID
    shipping_method_id: int
    order_total: Decimal
    order_status_id: int


class SOrders(BaseModel):
    orders: list[SOrder]


class SOrderWithLines(SOrder):
    products_in_order: list[SOrderLineWithoutOrder]
