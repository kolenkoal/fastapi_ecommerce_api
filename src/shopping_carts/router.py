from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.examples import example_shopping_cart
from src.exceptions import (
    ShoppingCartNotImplementedException,
    raise_http_exception,
)
from src.responses import UNAUTHORIZED_FORBIDDEN_RESPONSE
from src.shopping_carts.dao import ShoppingCartDAO
from src.shopping_carts.schemas import SShoppingCart, SShoppingCartCreate
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
