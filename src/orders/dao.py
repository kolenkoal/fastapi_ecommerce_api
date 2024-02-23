from src.dao import BaseDAO
from src.orders.models import ShopOrder
from src.users.models import User
from src.utils.session import manage_session


class ShopOrderDAO(BaseDAO):
    model = ShopOrder

    @classmethod
    @manage_session
    async def add(cls, user: User, data, session=None):
        data = data.model_dump(exclude_unset=True)

        # Validate all foreign keys exist
        # Check if cart is not empty
        # Validate quantity of every product
        # Count order_total
        # Add everything to order line
        # Clear shopping cart

        # existing_order_status = await cls.find_one_or_none(
        #     status=data["status"]
        # )
        #
        # if existing_order_status:
        #     raise_http_exception(OrderStatusAlreadyExistsException)
        #
        # return await cls._create(**data)
