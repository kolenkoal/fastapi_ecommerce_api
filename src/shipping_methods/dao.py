from sqlalchemy import select

from src.dao import BaseDAO
from src.exceptions import ForbiddenException, raise_http_exception
from src.permissions import has_permission
from src.shipping_methods.exceptions import (
    ShippingMethodAlreadyExistsException,
    ShippingMethodNotFoundException,
    ShippingMethodWithNameAlreadyExistsException,
)
from src.shipping_methods.models import ShippingMethod
from src.users.models import User
from src.utils.data_manipulation import get_new_data
from src.utils.session import manage_session


class ShippingMethodDAO(BaseDAO):
    model = ShippingMethod

    @classmethod
    @manage_session
    async def add(cls, user: User, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        existing_shipping_method = await cls.find_one_or_none(
            name=data["name"]
        )

        if existing_shipping_method:
            raise_http_exception(ShippingMethodAlreadyExistsException)

        return await cls._create(**data)

    @classmethod
    @manage_session
    async def find_all(cls, session=None):
        query = select(cls.model).order_by(cls.model.price)

        result = await session.execute(query)

        values = result.scalars().all()

        return values

    @classmethod
    @manage_session
    async def change(cls, shipping_method_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        current_shipping_method = await cls.find_one_or_none(
            id=shipping_method_id
        )

        if not current_shipping_method:
            return None

        if not data:
            return current_shipping_method

        new_product_category_data = get_new_data(current_shipping_method, data)

        existing_shipping_method = await cls.find_one_or_none(
            name=new_product_category_data["name"]
        )

        if (
            existing_shipping_method
            and existing_shipping_method.id != shipping_method_id
        ):
            raise_http_exception(ShippingMethodWithNameAlreadyExistsException)

        return await cls.update_data(shipping_method_id, data)

    @classmethod
    @manage_session
    async def delete(cls, user, shipping_method_id, session=None):
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Get current shipping method
        shipping_method = await cls.find_one_or_none(id=shipping_method_id)

        if not shipping_method:
            raise_http_exception(ShippingMethodNotFoundException)

        # Delete the shipping method
        await cls.delete_certain_item(shipping_method_id)
