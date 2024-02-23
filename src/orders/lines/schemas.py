from decimal import Decimal
from typing import Type, Union
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.exceptions import (
    PriceLessOrEqualZeroException,
    QuantityLessThanZeroException,
    WrongPriceException,
)


class SOrderLineCreate(BaseModel):
    product_item_id: UUID
    order_id: UUID
    quantity: int
    price: Decimal

    @field_validator("price")
    @classmethod
    def validate_price(
        cls, value
    ) -> Union[
        Decimal, Type[PriceLessOrEqualZeroException], Type[WrongPriceException]
    ]:
        if int(value) <= 0:
            raise PriceLessOrEqualZeroException

        return value

    @field_validator("quantity")
    @classmethod
    def validate_quantity_in_stock(
        cls, value
    ) -> Union[int, Type[QuantityLessThanZeroException],]:
        if int(value) < 0:
            raise QuantityLessThanZeroException

        return value


class SOrderLine(BaseModel):
    id: UUID
    product_item_id: UUID
    order_id: UUID
    quantity: int
    price: Decimal
