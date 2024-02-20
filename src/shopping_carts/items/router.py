from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.examples import example_shopping_cart_item
from src.exceptions import (
    ShoppingCartItemNotImplementedException,
    ShoppingCartItemsNotFoundException,
    raise_http_exception,
)
from src.responses import (
    UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_CART_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_NOT_FOUND_RESPONSE,
)
from src.shopping_carts.items.dao import ShoppingCartItemDAO
from src.shopping_carts.items.schemas import (
    SShoppingCartItem,
    SShoppingCartItemCreate,
)
from src.shopping_carts.schemas import SShoppingCartWithItems
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


@router.get(
    "",
    name="Get all carts",
    response_model=SShoppingCartWithItems,
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_NOT_FOUND_RESPONSE,
)
async def get_all_shopping_cart_items(
    shopping_cart_id: UUID, user: User = Depends(current_user)
):
    shopping_cart_items = await ShoppingCartItemDAO.find_all(
        user, shopping_cart_id
    )

    if not shopping_cart_items:
        raise_http_exception(ShoppingCartItemsNotFoundException)

    return shopping_cart_items
