from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.examples import example_shopping_cart
from src.exceptions import (
    ForbiddenException,
    ShoppingCartNotFoundException,
    ShoppingCartNotImplementedException,
    ShoppingCartsNotFoundException,
    raise_http_exception,
)
from src.permissions import has_permission
from src.responses import (
    CART_NOT_FOUND_RESPONSE,
    DELETED_UNAUTHORIZED_FORBIDDEN_CART_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_CART_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
    UNAUTHORIZED_FORBIDDEN_CARTS_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_RESPONSE,
)
from src.shopping_carts.dao import ShoppingCartDAO
from src.shopping_carts.schemas import (
    SShoppingCart,
    SShoppingCartCreate,
    SShoppingCarts,
)
from src.users.models import User


router = APIRouter(prefix="/shopping_carts", tags=["Shopping Carts"])


@router.post(
    "",
    name="Create a shopping cart for a user",
    response_model=SShoppingCart,
    responses=UNAUTHORIZED_FORBIDDEN_RESPONSE,
)
async def create_shopping_cart(
    shopping_cart_data: SShoppingCartCreate = example_shopping_cart,
    user: User = Depends(current_user),
):
    cart = await ShoppingCartDAO.add(shopping_cart_data, user)

    if not cart:
        raise_http_exception(ShoppingCartNotImplementedException)

    return cart


@router.get(
    "",
    name="Get all carts",
    response_model=Union[SShoppingCart, SShoppingCarts],
    responses=UNAUTHORIZED_FORBIDDEN_CARTS_NOT_FOUND_RESPONSE,
)
async def get_all_shopping_carts(user: User = Depends(current_user)):
    shopping_carts = await ShoppingCartDAO.find_all(user)

    if not shopping_carts:
        raise_http_exception(ShoppingCartsNotFoundException)

    return shopping_carts


@router.get(
    "/{shopping_cart_id}",
    name="Get certain shopping cart.",
    response_model=SShoppingCart,
    responses=CART_NOT_FOUND_RESPONSE,
)
async def get_shopping_cart(
    shopping_cart_id: UUID, user: User = Depends(current_user)
):
    shopping_cart = await ShoppingCartDAO.find_by_id(shopping_cart_id)

    if not shopping_cart:
        raise_http_exception(ShoppingCartNotFoundException)

    if shopping_cart.user_id != user.id:
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

    return shopping_cart


@router.patch(
    "/{shopping_cart_id}",
    response_model=SShoppingCart,
    name="Change certain shopping cart.",
    responses=UNAUTHORIZED_FORBIDDEN_CART_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
async def change_variation(
    shopping_cart_id: UUID,
    data: SShoppingCartCreate,
    user: User = Depends(current_user),
):
    shopping_cart = await ShoppingCartDAO.change(shopping_cart_id, user, data)

    if not shopping_cart:
        raise_http_exception(ShoppingCartNotFoundException)

    return shopping_cart


@router.delete(
    "/{shopping_cart_id}",
    name="Delete certain shopping cart.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_CART_NOT_FOUND_RESPONSE,
)
async def delete_variation(
    shopping_cart_id: UUID,
    user: User = Depends(current_user),
):
    shopping_cart = await ShoppingCartDAO.delete(user, shopping_cart_id)

    if not shopping_cart:
        return {"detail": "The shopping_cart was deleted."}
