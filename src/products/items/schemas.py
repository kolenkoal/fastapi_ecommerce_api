from decimal import Decimal
from typing import Type, Union
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.exceptions import (
    PriceLessOrEqualZeroException,
    QuantityLessThanZeroException,
    WrongPriceException,
    WrongQuantityException,
)


class SProductItemCreate(BaseModel):
    price: Decimal
    quantity_in_stock: int
    product_id: UUID

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

    @field_validator("quantity_in_stock")
    @classmethod
    def validate_quantity_in_stock(
        cls, value
    ) -> Union[
        Decimal,
        Type[QuantityLessThanZeroException],
        Type[WrongQuantityException],
    ]:
        if int(value) < 0:
            raise QuantityLessThanZeroException

        return value


class SProductItem(BaseModel):
    id: UUID
    price: Decimal
    SKU: str
    quantity_in_stock: int
    product_id: UUID
    product_image: str
