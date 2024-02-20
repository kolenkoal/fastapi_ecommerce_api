from uuid import UUID

from pydantic import BaseModel


class SShoppingCartItemCreate(BaseModel):
    product_item_id: UUID


class SShoppingCartItem(BaseModel):
    id: UUID
    cart_id: UUID
    product_item_id: UUID
    quantity: int
