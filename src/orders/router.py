from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.exceptions import ShopOrderNotImplementedException
from src.orders.dao import ShopOrderDAO
from src.orders.lines.router import router as router_lines
from src.orders.schemas import SShopOrder, SShopOrderCreate
from src.orders.statuses.router import router as router_statuses
from src.responses import (
    UNAUTHORIZED_PAYMENT_OR_SHIPPING_METHOD_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE,
)
from src.users.models import User


router = APIRouter(prefix="/orders", tags=["Orders"])

router.include_router(router_statuses)
router.include_router(router_lines)


@router.post(
    "",
    name="Create order.",
    response_model=SShopOrder,
    responses=UNAUTHORIZED_PAYMENT_OR_SHIPPING_METHOD_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE,
)
async def create_shop_order(
    shop_order_data: SShopOrderCreate, user: User = Depends(current_user)
):
    shop_order = await ShopOrderDAO.add(user, shop_order_data)

    if not shop_order:
        raise ShopOrderNotImplementedException

    return shop_order
