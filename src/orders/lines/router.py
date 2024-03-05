from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.orders.lines.dao import OrderLineDAO
from src.orders.lines.exceptions import OrderLineNotFoundException
from src.orders.lines.schemas import SOrderLineCreate
from src.users.models import User


router = APIRouter(prefix="/{order_id}/lines")


async def create_order_line(
    order_id: UUID,
    order_line_data: SOrderLineCreate,
    user: User = Depends(current_user),
):
    order_line = await OrderLineDAO.add(user, order_id, order_line_data)

    if not order_line:
        raise OrderLineNotFoundException

    return order_line
