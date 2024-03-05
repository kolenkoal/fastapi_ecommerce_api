from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.exceptions import OrderLinesNotFoundException, raise_http_exception
from src.orders.dao import OrderDAO
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
async def create_order(
    order_data: SOrderCreate, user: User = Depends(current_user)
):
    order = await OrderDAO.add(user, order_data)

    if not order:
        raise OrderNotImplementedException

    return order


@router.get(
    "",
    name="Get user orders.",
    response_model=SOrders,
    responses=UNAUTHORIZED_ORDERS_NOT_FOUND,
)
async def get_user_orders(user: User = Depends(current_user)):
    orders = await OrderDAO.find_all(user)

    if not orders:
        raise OrdersNotFoundException

    return {"orders": orders}


@router.get(
    "/{order_id}/lines",
    name="Get user order lines.",
    response_model=SOrderWithLines,
    responses=UNAUTHORIZED_FORBIDDEN_ORDER_LINES_NOT_FOUND,
)
async def get_user_order_lines(
    order_id: UUID, user: User = Depends(current_user)
):
    order_with_lines = await OrderDAO.find_order_lines(order_id, user)

    if not order_with_lines:
        raise OrderLinesNotFoundException

    return order_with_lines


@router.get(
    "/{order_id}",
    name="Get certain product order status.",
    response_model=SOrder,
    responses=UNAUTHORIZED_ORDER_NOT_FOUND,
)
async def get_order(order_id: UUID):
    order = await OrderDAO.find_one_or_none(id=order_id)

    if not order:
        raise_http_exception(OrderNotFoundException)

    return order


@router.patch(
    "/{order_id}",
    name="Change certain shop order.",
    response_model=SOrder,
    responses=UNAUTHORIZED_FORBIDDEN_ORDER_NOT_FOUND,
)
async def change_order_status(
    order_id: UUID,
    data: SOrderChangeOptional,
    user: User = Depends(current_user),
):
    order = await OrderDAO.change(order_id, user, data)

    if not order:
        raise OrderNotFoundException

    return order


@router.delete(
    "/{order_id}",
    name="Delete certain order.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_ORDER_NOT_FOUND,
)
async def delete_order_status(
    order_id: UUID,
    user: User = Depends(current_user),
):
    order = await OrderDAO.delete(user, order_id)

    if not order:
        return {"detail": "The order was deleted."}
