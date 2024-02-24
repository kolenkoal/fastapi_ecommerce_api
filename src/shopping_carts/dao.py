from sqlalchemy import select

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    ShoppingCartAlreadyExistsException,
    ShoppingCartNotFoundException,
    ShoppingCartsNotFoundException,
    UserAlreadyHasCartException,
    raise_http_exception,
)
from src.permissions import has_permission
from src.shopping_carts.models import ShoppingCart
from src.users.models import User
from src.utils.data_manipulation import get_new_data
from src.utils.session import manage_session


class ShoppingCartDAO(BaseDAO):
    model = ShoppingCart

    @classmethod
    @manage_session
    async def add(cls, shopping_cart_data, user, session=None):
        shopping_cart_data = shopping_cart_data.model_dump()

        await cls._check_cart_exists(user)

        return await cls._create(**shopping_cart_data)

    @classmethod
    @manage_session
    async def _check_cart_exists(cls, user, session=None):
        cart = await cls.find_one_or_none(user_id=user.id)

        if cart:
            raise_http_exception(UserAlreadyHasCartException)

    @classmethod
    @manage_session
    async def find_all(cls, user: User, session=None):
        if not await has_permission(user):
            get_cart_query = select(cls.model).where(
                cls.model.user_id == user.id
            )

            cart_result = await session.execute(get_cart_query)

            shopping_cart = cart_result.scalar_one_or_none()

            return shopping_cart

        else:
            get_all_carts_query = select(cls.model)

            all_carts_result = await session.execute(get_all_carts_query)

            shopping_carts = all_carts_result.scalars().all()

            if not shopping_carts:
                raise_http_exception(ShoppingCartsNotFoundException)

            return {"shopping_carts": shopping_carts}

    @classmethod
    @manage_session
    async def change(cls, shopping_cart_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        current_shopping_cart = await cls.find_one_or_none(id=shopping_cart_id)

        if not current_shopping_cart:
            return None

        if not data:
            return current_shopping_cart

        if "user_id" in data:
            if data["user_id"] is not None:
                await cls._check_user_by_id(data["user_id"])

        new_shopping_cart_data = get_new_data(current_shopping_cart, data)

        existing_shopping_cart = await cls.find_one_or_none(
            user_id=new_shopping_cart_data["user_id"]
        )

        if existing_shopping_cart.id != shopping_cart_id:
            raise_http_exception(ShoppingCartAlreadyExistsException)

        return await cls.update_data(shopping_cart_id, new_shopping_cart_data)

    @classmethod
    @manage_session
    async def _check_user_by_id(cls, user_id, session=None):
        query = select(User).where(user_id == User.id)

        result = await session.execute(query)

        return result.scalar_one_or_none()

    @classmethod
    @manage_session
    async def delete(cls, user, shopping_cart_id, session=None):
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Get current shopping cart
        shopping_cart = await cls.validate_by_id(shopping_cart_id)

        if not shopping_cart:
            raise_http_exception(ShoppingCartNotFoundException)

        # Delete the shopping cart
        await cls.delete_certain_item(shopping_cart_id)
