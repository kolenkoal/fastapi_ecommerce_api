from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.exceptions import (
    ShopOrderNotFoundException,
    ShopOrderNotImplementedException,
    ShopOrdersNotFoundException,
    raise_http_exception,
)
from src.orders.dao import ShopOrderDAO
from src.orders.lines.router import router as router_lines
from src.orders.schemas import (
    SShopOrder,
    SShopOrderChangeOptional,
    SShopOrderCreate,
    SShopOrders,
)
from src.orders.statuses.router import router as router_statuses
from src.responses import (
    DELETED_UNAUTHORIZED_SHOP_ORDER_NOT_FOUND,
    UNAUTHORIZED_FORBIDDEN_SHOP_ORDER_NOT_FOUND,
    UNAUTHORIZED_PAYMENT_OR_SHIPPING_METHOD_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE,
    UNAUTHORIZED_SHOP_ORDER_NOT_FOUND,
    UNAUTHORIZED_SHOP_ORDERS_NOT_FOUND,
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


@router.get(
    "",
    name="Get user orders.",
    response_model=SShopOrders,
    responses=UNAUTHORIZED_SHOP_ORDERS_NOT_FOUND,
)
async def get_user_shop_orders(user: User = Depends(current_user)):
    shop_orders = await ShopOrderDAO.find_all(user)

    if not shop_orders:
        raise ShopOrdersNotFoundException

    return {"shop_orders": shop_orders}


@router.get(
    "/{shop_order_id}",
    name="Get certain product order status.",
    response_model=SShopOrder,
    responses=UNAUTHORIZED_SHOP_ORDER_NOT_FOUND,
)
async def get_shop_order(shop_order_id: UUID):
    shop_order = await ShopOrderDAO.find_one_or_none(id=shop_order_id)

    if not shop_order:
        raise_http_exception(ShopOrderNotFoundException)

    return shop_order


@router.patch(
    "/{shop_order_id}",
    name="Change certain shop order.",
    response_model=SShopOrder,
    responses=UNAUTHORIZED_FORBIDDEN_SHOP_ORDER_NOT_FOUND,
)
async def change_order_status(
    shop_order_id: UUID,
    data: SShopOrderChangeOptional,
    user: User = Depends(current_user),
):
    shop_order = await ShopOrderDAO.change(shop_order_id, user, data)

    if not shop_order:
        raise ShopOrderNotFoundException

    return shop_order


@router.delete(
    "/{shop_order_id}",
    name="Delete certain order.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_SHOP_ORDER_NOT_FOUND,
)
async def delete_order_status(
    shop_order_id: UUID,
    user: User = Depends(current_user),
):
    shop_order = await ShopOrderDAO.delete(user, shop_order_id)

    if not shop_order:
        return {"detail": "The order was deleted."}
