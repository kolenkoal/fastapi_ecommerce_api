from decimal import Decimal
from typing import Optional, Type, Union

from pydantic import BaseModel, field_validator

from src.exceptions import (
    PriceLessOrEqualZeroException,
    WrongPaymentTypeNameException,
    WrongPriceException,
)
from src.patterns import LETTER_MATCH_PATTERN


class SShippingMethodCreate(BaseModel):
    name: str
    price: Decimal

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str):
        if not LETTER_MATCH_PATTERN.match(name):
            raise WrongPaymentTypeNameException

        return name.title()

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


class SShippingMethod(BaseModel):
    id: int
    name: str
    price: Decimal


class SShippingMethodCreateOptional(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str):
        if not LETTER_MATCH_PATTERN.match(name):
            raise WrongPaymentTypeNameException

        return name.title()

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


class SShippingMethods(BaseModel):
    shipping_methods: list[SShippingMethod]
