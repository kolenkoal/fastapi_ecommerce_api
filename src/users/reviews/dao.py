from sqlalchemy import select

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    OrderLineNotFoundException,
    raise_http_exception,
)
from src.orders.lines.dao import OrderLineDAO
from src.orders.lines.models import OrderLine
from src.orders.models import ShopOrder
from src.users.models import User
from src.users.reviews.models import UserReview
from src.utils.session import manage_session


class UserReviewDAO(BaseDAO):
    model = UserReview

    @classmethod
    @manage_session
    async def add(cls, user: User, review_data, session=None):
        review_data = review_data.model_dump(exclude_unset=True)

        # Find ordered product
        ordered_product = await OrderLineDAO.find_one_or_none(
            id=review_data["ordered_product_id"]
        )

        if not ordered_product:
            raise_http_exception(OrderLineNotFoundException)

        # Validate user ordered this product
        await cls._validate_user_ordered_product(ordered_product.id, user)

        # Add data with needed values
        review_data.update({"user_id": user.id})

        # Create review
        user_review = await cls._create(**review_data)

        if not user_review:
            return None

        return user_review

    @classmethod
    @manage_session
    async def _validate_user_ordered_product(
        cls, ordered_product_id, user, session=None
    ):
        query = (
            select(ShopOrder.user_id)
            .join(OrderLine, ShopOrder.id == OrderLine.order_id)
            .where(OrderLine.id == ordered_product_id)
        )

        result = await session.execute(query)

        user_id = result.scalar_one_or_none()

        if user_id != user.id:
            raise_http_exception(ForbiddenException)
