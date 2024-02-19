from src.dao import BaseDAO
from src.exceptions import UserAlreadyHasCartException, raise_http_exception
from src.shopping_carts.models import ShoppingCart
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
