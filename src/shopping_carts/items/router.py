from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.examples import example_shopping_cart_item
from src.exceptions import (
    ShoppingCartItemNotImplementedException,
    raise_http_exception,
)
from src.responses import (
    UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_CART_NOT_FOUND_RESPONSE,
)
from src.shopping_carts.items.dao import ShoppingCartItemDAO
from src.shopping_carts.items.schemas import (
    SShoppingCartItem,
    SShoppingCartItemCreate,
)
from src.users.models import User


router = APIRouter(prefix="/{shopping_cart_id}/items")


@router.post(
    "",
    name="Add item to the cart",
    response_model=SShoppingCartItem,
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_CART_NOT_FOUND_RESPONSE,
)
async def create_shopping_cart_item(
    shopping_cart_id: UUID,
    shopping_cart_item_data: SShoppingCartItemCreate = example_shopping_cart_item,
    user: User = Depends(current_user),
):
    shopping_cart_item = await ShoppingCartItemDAO.add(
        shopping_cart_id, shopping_cart_item_data, user
    )

    if not shopping_cart_item:
        raise_http_exception(ShoppingCartItemNotImplementedException)

    return shopping_cart_item
