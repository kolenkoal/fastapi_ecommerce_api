from uuid import UUID

from pydantic import BaseModel, field_validator

from src.exceptions import QuantityLessThanOneException, WrongQuantityException
from src.patterns import NUMBER_PATTERN


class SShoppingCartItemCreate(BaseModel):
    product_item_id: UUID


class SShoppingCartItem(BaseModel):
    id: UUID
    cart_id: UUID
    product_item_id: UUID
    quantity: int


class SShoppingCartItemQuantity(BaseModel):
    product_item_id: UUID
    quantity: int


class ShoppingCartItemChange(BaseModel):
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int):
        if not NUMBER_PATTERN.match(value):
            raise WrongQuantityException

        if value < 1:
            raise QuantityLessThanOneException

        return value
