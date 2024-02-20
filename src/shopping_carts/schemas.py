from uuid import UUID

from pydantic import BaseModel

from src.shopping_carts.items.schemas import SShoppingCartItemQuantity


class SShoppingCartCreate(BaseModel):
    user_id: UUID


class SShoppingCart(BaseModel):
    id: UUID
    user_id: UUID


class SShoppingCarts(BaseModel):
    shopping_carts: list[SShoppingCart]


class SShoppingCartWithItems(BaseModel):
    id: UUID
    user_id: UUID
    cart_items: list[SShoppingCartItemQuantity]
