from decimal import Decimal
from typing import Optional, Type, Union
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.exceptions import (
    PriceLessOrEqualZeroException,
    QuantityLessThanZeroException,
    WrongPriceException,
    WrongQuantityException,
)
from src.products.schemas import SProduct
from src.variation_options.schemas import SVariationOption


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


class SProductItemCreateOptional(BaseModel):
    price: Optional[Decimal] = None
    quantity_in_stock: Optional[int] = None
    product_id: Optional[UUID] = None

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


class SProductItemWithProduct(BaseModel):
    id: UUID
    price: Decimal
    SKU: str
    quantity_in_stock: int
    product_image: str
    product: SProduct


class SProductWithItems(SProduct):
    product_items: list[SProductItem]


class SProductItemWithVariations(SProductItem):
    variations: list[SVariationOption]


class SProductItems(BaseModel):
    product_items: list[SProductItem]
