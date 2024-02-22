from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.examples import example_shopping_cart_item
from src.exceptions import (
    ShoppingCartItemNotFoundException,
    ShoppingCartItemNotImplementedException,
    ShoppingCartItemsNotFoundException,
    raise_http_exception,
)
from src.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_CART_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_OR_SHOPPING_CART_ITEM_NOT_FOUND_RESPONSE,
)
from src.shopping_carts.items.dao import ShoppingCartItemDAO
from src.shopping_carts.items.schemas import (
    ShoppingCartItemChange,
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
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_OR_SHOPPING_CART_ITEM_NOT_FOUND_RESPONSE,
)
async def get_all_shopping_cart_items(
    shopping_cart_id: UUID, user: User = Depends(current_user)
):
    shopping_cart_items = await ShoppingCartItemDAO.find_all(
        user, shopping_cart_id
    )

    if not shopping_cart_items:
        raise_http_exception(ShoppingCartItemsNotFoundException)

    if not shopping_cart_items.__dict__["cart_items"]:
        raise_http_exception(ShoppingCartItemsNotFoundException)

    return shopping_cart_items


@router.patch(
    "/{shopping_cart_item_id}",
    response_model=SShoppingCartItem,
    name="Change certain shopping cart item.",
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_NOT_FOUND_RESPONSE,
)
async def change_shopping_cart_item(
    shopping_cart_id: UUID,
    shopping_cart_item_id: UUID,
    data: ShoppingCartItemChange,
    user: User = Depends(current_user),
):
    shopping_cart_item = await ShoppingCartItemDAO.change(
        shopping_cart_id, shopping_cart_item_id, user, data
    )

    if not shopping_cart_item:
        raise_http_exception(ShoppingCartItemNotFoundException)

    return shopping_cart_item


@router.delete(
    "/{shopping_cart_item_id}",
    name="Delete certain shopping cart.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_NOT_FOUND_RESPONSE,
)
async def delete_shopping_cart_item(
    shopping_cart_id: UUID,
    shopping_cart_item_id: UUID,
    user: User = Depends(current_user),
):
    shopping_cart = await ShoppingCartItemDAO.delete(
        user, shopping_cart_id, shopping_cart_item_id
    )

    if not shopping_cart:
        return {"detail": "The shopping cart item was deleted."}
