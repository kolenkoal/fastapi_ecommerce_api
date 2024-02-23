from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class SShopOrderCreate(BaseModel):
    payment_method_id: UUID
    shipping_address_id: UUID
    shipping_method_id: int


class SShopOrder(BaseModel):
    id: UUID
    user_id: UUID
    order_date: date
    payment_method_id: UUID
    shipping_address_id: UUID
    shipping_method_id: int
    order_total: Decimal
    order_status_id: int
