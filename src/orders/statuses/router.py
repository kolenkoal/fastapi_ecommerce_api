from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.examples import example_order_status
from src.exceptions import (
    OrderStatusesNotFoundException,
    OrderStatusNotFoundException,
    OrderStatusNotImplementedException,
    raise_http_exception,
)
from src.orders.statuses.dao import OrderStatusDAO
from src.orders.statuses.schemas import (
    SOrderStatus,
    SOrderStatusCreate,
    SOrderStatusCreateOptional,
    SOrderStatuses,
)
from src.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE,
    ORDER_STATUS_NOT_FOUND_RESPONSE,
    ORDER_STATUSES_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_UNPROCESSABLE_RESPONSE,
)
from src.users.models import User


router = APIRouter(prefix="/statuses")


@router.post(
    "",
    response_model=SOrderStatus,
    name="Add order status.",
    responses=UNAUTHORIZED_FORBIDDEN_UNPROCESSABLE_RESPONSE,
)
async def add_order_status(
    order_status_data: SOrderStatusCreate = example_order_status,
    user: User = Depends(current_user),
):
    order_status = await OrderStatusDAO.add(user, order_status_data)

    if not order_status:
        raise OrderStatusNotImplementedException

    return order_status


@router.get(
    "",
    name="Get all order_statuses.",
    response_model=SOrderStatuses,
    responses=ORDER_STATUSES_NOT_FOUND_RESPONSE,
)
async def get_all_order_statuses():
    order_statuses = await OrderStatusDAO.find_all()

    if not order_statuses:
        raise OrderStatusesNotFoundException

    return {"order_statuses": order_statuses}


@router.get(
    "/{order_status_id}",
    name="Get certain product order status.",
    response_model=SOrderStatus,
    responses=ORDER_STATUS_NOT_FOUND_RESPONSE,
)
async def get_order_status(order_status_id: int):
    order_status = await OrderStatusDAO.find_one_or_none(id=order_status_id)

    if not order_status:
        raise_http_exception(OrderStatusNotFoundException)

    return order_status


@router.patch(
    "/{order_status_id}",
    name="Change certain order status.",
    response_model=SOrderStatus,
    responses=UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE,
)
async def change_order_status(
    order_status_id: int,
    data: SOrderStatusCreateOptional,
    user: User = Depends(current_user),
):
    order_status = await OrderStatusDAO.change(order_status_id, user, data)

    if not order_status:
        raise OrderStatusNotFoundException

    return order_status


@router.delete(
    "/{order_status_id}",
    name="Delete certain order status.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE,
)
async def delete_order_status(
    order_status_id: int,
    user: User = Depends(current_user),
):
    order_status = await OrderStatusDAO.delete(user, order_status_id)

    if not order_status:
        return {"detail": "The order status was deleted."}
