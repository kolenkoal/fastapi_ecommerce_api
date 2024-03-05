from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.exceptions import OrderLinesNotFoundException, raise_http_exception
from src.orders.dao import ShopOrderDAO
from src.orders.exceptions import (
    OrderNotFoundException,
    OrderNotImplementedException,
    OrdersNotFoundException,
)
from src.orders.lines.router import router as router_lines
from src.orders.responses import (
    DELETED_UNAUTHORIZED_ORDER_NOT_FOUND,
    UNAUTHORIZED_FORBIDDEN_ORDER_NOT_FOUND,
    UNAUTHORIZED_ORDER_NOT_FOUND,
    UNAUTHORIZED_ORDERS_NOT_FOUND,
    UNAUTHORIZED_PAYMENT_OR_SHIPPING_METHOD_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE,
)
from src.orders.schemas import (
    SOrder,
    SOrderChangeOptional,
    SOrderCreate,
    SOrders,
    SOrderWithLines,
)
from src.orders.statuses.router import router as router_statuses
from src.responses import UNAUTHORIZED_FORBIDDEN_ORDER_LINES_NOT_FOUND
from src.users.models import User


router = APIRouter(prefix="/orders", tags=["Orders"])

router.include_router(router_statuses)
router.include_router(router_lines)


@router.post(
    "",
    name="Create order.",
    response_model=SOrder,
    responses=UNAUTHORIZED_PAYMENT_OR_SHIPPING_METHOD_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE,
)
async def create_shop_order(
    shop_order_data: SOrderCreate, user: User = Depends(current_user)
):
    shop_order = await ShopOrderDAO.add(user, shop_order_data)

    if not shop_order:
        raise OrderNotImplementedException

    return shop_order


@router.get(
    "",
    name="Get user orders.",
    response_model=SOrders,
    responses=UNAUTHORIZED_ORDERS_NOT_FOUND,
)
async def get_user_shop_orders(user: User = Depends(current_user)):
    shop_orders = await ShopOrderDAO.find_all(user)

    if not shop_orders:
        raise OrdersNotFoundException

    return {"shop_orders": shop_orders}


@router.get(
    "/{order_id}/lines",
    name="Get user order lines.",
    response_model=SOrderWithLines,
    responses=UNAUTHORIZED_FORBIDDEN_ORDER_LINES_NOT_FOUND,
)
async def get_user_order_lines(
    order_id: UUID, user: User = Depends(current_user)
):
    order_with_lines = await ShopOrderDAO.find_shop_order_lines(order_id, user)

    if not order_with_lines:
        raise OrderLinesNotFoundException

    return order_with_lines


@router.get(
    "/{shop_order_id}",
    name="Get certain product order status.",
    response_model=SOrder,
    responses=UNAUTHORIZED_ORDER_NOT_FOUND,
)
async def get_shop_order(shop_order_id: UUID):
    shop_order = await ShopOrderDAO.find_one_or_none(id=shop_order_id)

    if not shop_order:
        raise_http_exception(OrderNotFoundException)

    return shop_order


@router.patch(
    "/{shop_order_id}",
    name="Change certain shop order.",
    response_model=SOrder,
    responses=UNAUTHORIZED_FORBIDDEN_ORDER_NOT_FOUND,
)
async def change_order_status(
    shop_order_id: UUID,
    data: SOrderChangeOptional,
    user: User = Depends(current_user),
):
    shop_order = await ShopOrderDAO.change(shop_order_id, user, data)

    if not shop_order:
        raise OrderNotFoundException

    return shop_order


@router.delete(
    "/{shop_order_id}",
    name="Delete certain order.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_ORDER_NOT_FOUND,
)
async def delete_order_status(
    shop_order_id: UUID,
    user: User = Depends(current_user),
):
    shop_order = await ShopOrderDAO.delete(user, shop_order_id)

    if not shop_order:
        return {"detail": "The order was deleted."}
