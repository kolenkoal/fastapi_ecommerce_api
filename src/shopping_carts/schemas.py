from uuid import UUID

from pydantic import BaseModel


class SShoppingCartCreate(BaseModel):
    user_id: UUID


class SShoppingCart(BaseModel):
    id: UUID
    user_id: UUID
