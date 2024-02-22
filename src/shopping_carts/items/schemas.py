from uuid import UUID

from pydantic import BaseModel, field_validator

from src.exceptions import QuantityLessThanOneException


class SShoppingCartItemCreate(BaseModel):
    product_item_id: UUID


class SShoppingCartItem(BaseModel):
    id: UUID
    cart_id: UUID
    product_item_id: UUID
    quantity: int


class SShoppingCartItemQuantity(BaseModel):
    id: UUID
    quantity: int


class ShoppingCartItemChange(BaseModel):
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int):
        if value < 1:
            raise QuantityLessThanOneException

        return value
