from sqlalchemy import select

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    OrderLineNotFoundException,
    UserReviewAlreadyExistsException,
    UserReviewNotFoundException,
    raise_http_exception,
)
from src.orders.lines.dao import OrderLineDAO
from src.orders.lines.models import OrderLine
from src.orders.models import Order
from src.users.models import User
from src.users.reviews.models import UserReview
from src.utils.data_manipulation import get_new_data
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

        existing_user_review = await cls.find_one_or_none(
            ordered_product_id=review_data["ordered_product_id"]
        )

        if existing_user_review:
            raise_http_exception(UserReviewAlreadyExistsException)

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
            select(Order.user_id)
            .join(OrderLine, Order.id == OrderLine.order_id)
            .where(OrderLine.id == ordered_product_id)
        )

        result = await session.execute(query)

        user_id = result.scalar_one_or_none()

        if user_id != user.id:
            raise_http_exception(ForbiddenException)

    @classmethod
    @manage_session
    async def find_all(cls, user, session=None):
        query = (
            select(cls.model)
            .where(cls.model.user_id == user.id)
            .order_by(cls.model.rating_value)
        )

        result = await session.execute(query)

        values = result.scalars().all()

        return values

    @classmethod
    @manage_session
    async def change(cls, user_review_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        current_user_review = await cls.find_one_or_none(id=user_review_id)

        if not current_user_review:
            return None

        if current_user_review.user_id != user.id:
            raise_http_exception(ForbiddenException)

        if not data:
            return current_user_review

        new_user_review_data = get_new_data(current_user_review, data)

        existing_user_review = await cls.find_one_or_none(
            **new_user_review_data
        )

        if existing_user_review and existing_user_review.id != user_review_id:
            raise_http_exception(UserReviewAlreadyExistsException)

        return await cls.update_data(user_review_id, data)

    @classmethod
    @manage_session
    async def delete(cls, user, user_review_id, session=None):
        # Get current user review
        user_review = await cls.validate_by_id(user_review_id)

        if not user_review:
            raise_http_exception(UserReviewNotFoundException)

        if user_review.user_id != user.id:
            raise_http_exception(ForbiddenException)

        # Delete the user review
        await cls.delete_certain_item(user_review_id)
