from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dao import BaseDAO
from src.exceptions import ForbiddenException, raise_http_exception
from src.permissions import has_permission
from src.products.categories.exceptions import (
    ParentCategoryNotFoundException,
    ProductCategoryAlreadyExistsException,
    ProductCategoryParentNotAllowed,
)
from src.products.categories.models import ProductCategory
from src.users.models import User
from src.utils.data_manipulation import get_new_data
from src.utils.session import manage_session


class ProductCategoryDAO(BaseDAO):
    model = ProductCategory

    @classmethod
    @manage_session
    async def add(cls, user: User, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        if "parent_category_id" in data:
            if data["parent_category_id"] is not None:
                await cls._check_parent_category_by_id(
                    data["parent_category_id"]
                )

        existing_category = await cls.find_one_or_none(**data)

        if existing_category:
            raise_http_exception(ProductCategoryAlreadyExistsException)

        return await cls._create(**data)

    @classmethod
    @manage_session
    async def _check_parent_category_by_id(
        cls, parent_category_id, session=None
    ):
        get_parent_category_query = select(cls.model).where(
            cls.model.id == parent_category_id
        )

        parent_category = (
            await session.execute(get_parent_category_query)
        ).scalar_one_or_none()

        if not parent_category:
            raise_http_exception(ParentCategoryNotFoundException)

    @classmethod
    @manage_session
    async def find_all(cls, session=None):
        query = select(cls.model).order_by(cls.model.id)

        result = await session.execute(query)

        values = result.scalars().all()

        return values

    @classmethod
    @manage_session
    async def find_by_id_and_children(cls, model_id, session=None) -> model:
        query = (
            select(cls.model)
            .options(joinedload(cls.model.children_categories))
            .filter_by(id=model_id)
        )

        result = await session.execute(query)

        return result.unique().mappings().one_or_none()["ProductCategory"]

    @classmethod
    @manage_session
    async def change(cls, product_category_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        current_category = await cls._find_product_category_by_id(
            product_category_id
        )

        if not current_category:
            return None

        if not data:
            return current_category

        if "parent_category_id" in data:
            if data["parent_category_id"] is not None:
                await cls._check_parent_category_by_id(
                    data["parent_category_id"]
                )
                if current_category.id == data["parent_category_id"]:
                    raise_http_exception(ProductCategoryParentNotAllowed)

        new_product_category_data = get_new_data(current_category, data)

        existing_category = await cls.find_one_or_none(
            **new_product_category_data
        )

        if existing_category:
            raise_http_exception(ProductCategoryAlreadyExistsException)

        return await cls.update_data(product_category_id, data)

    @classmethod
    @manage_session
    async def _find_product_category_by_id(
        cls, product_category_id, session=None
    ):
        get_product_category_query = select(cls.model).where(
            cls.model.id == product_category_id
        )
        product_category = (
            await session.execute(get_product_category_query)
        ).scalar_one_or_none()

        return product_category

    @classmethod
    @manage_session
    async def delete(cls, user, product_category_id, session=None):
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Get current product category
        current_category = await cls._find_product_category_by_id(
            product_category_id
        )

        if not current_category:
            return None

        # Delete the product category
        await cls.delete_certain_item(product_category_id)

    @classmethod
    @manage_session
    async def get_product_category_variations(
        cls, product_category_id, session=None
    ):
        query = (
            select(cls.model)
            .options(joinedload(cls.model.variations))
            .filter_by(id=product_category_id)
        )

        result = await session.execute(query)

        product_category = (
            result.unique().mappings().one_or_none()["ProductCategory"]
        )

        return product_category

    @classmethod
    @manage_session
    async def get_product_category_products(
        cls, product_category_id, session=None
    ):
        query = (
            select(cls.model)
            .options(joinedload(cls.model.products))
            .filter_by(id=product_category_id)
        )

        result = await session.execute(query)

        product_category = (
            result.unique().mappings().one_or_none()["ProductCategory"]
        )

        return product_category
