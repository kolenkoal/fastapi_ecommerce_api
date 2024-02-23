from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.exceptions import OrderLineNotFoundException
from src.orders.lines.dao import OrderLineDAO
from src.orders.lines.schemas import SOrderLine, SOrderLineCreate
from src.responses import (
    UNAUTHORIZED_PRODUCT_ITEM_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE,
)
from src.users.models import User


router = APIRouter(prefix="/lines")


@router.post(
    "",
    name="Create order line.",
    response_model=SOrderLine,
    responses=UNAUTHORIZED_PRODUCT_ITEM_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE,
)
async def create_order_line(
    order_line_data: SOrderLineCreate, user: User = Depends(current_user)
):
    order_line = await OrderLineDAO.add(user, order_line_data)

    if not order_line:
        raise OrderLineNotFoundException

    return order_line
