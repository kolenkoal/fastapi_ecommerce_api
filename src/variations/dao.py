from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dao import BaseDAO
from src.exceptions import ForbiddenException, raise_http_exception
from src.permissions import has_permission
from src.products.categories.dao import ProductCategoryDAO
from src.products.categories.exceptions import ProductCategoryNotFoundException
from src.products.categories.models import ProductCategory
from src.utils.data_manipulation import get_new_data
from src.utils.session import manage_session
from src.variations.exceptions import (
    VariationAlreadyExistsException,
    VariationNotFoundException,
)
from src.variations.models import Variation


class VariationDAO(BaseDAO):
    model = Variation

    @classmethod
    @manage_session
    async def add(cls, user, variation_data, session=None):
        variation_data = variation_data.model_dump()

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        await cls._validate_category_by_id(variation_data["category_id"])

        existing_variation = await cls.find_one_or_none(**variation_data)

        if existing_variation:
            raise_http_exception(VariationAlreadyExistsException)

        new_variation = await cls._create(**variation_data)

        await cls._add_to_children_categories(
            variation_data["category_id"], new_variation
        )
        return new_variation

    @classmethod
    @manage_session
    async def _validate_category_by_id(cls, category_id, session=None):
        product_category = await ProductCategoryDAO.find_by_id(category_id)

        if not product_category:
            raise_http_exception(ProductCategoryNotFoundException)

    @classmethod
    @manage_session
    async def _add_to_children_categories(
        cls, category_id, variation, session=None
    ):
        query = (
            select(ProductCategory)
            .options(joinedload(ProductCategory.children_categories))
            .filter_by(id=category_id)
        )
        result = await session.execute(query)
        category = result.scalars().unique().one_or_none()

        if category and category.children_categories:
            for child_category in category.children_categories:
                child_variation_data = {
                    "name": variation.name,
                    "category_id": child_category.id,
                }
                child_variation = Variation(**child_variation_data)
                existing_variation = await cls.find_one_or_none(
                    **child_variation_data
                )
                if not existing_variation:
                    await cls._create(**child_variation_data)
                    await cls._add_to_children_categories(
                        child_category.id, child_variation
                    )

    @classmethod
    @manage_session
    async def find_all(cls, session=None):
        query = select(cls.model).order_by(cls.model.category_id)

        result = await session.execute(query)

        values = result.scalars().all()

        return values

    @classmethod
    @manage_session
    async def find_by_id(cls, model_id, session=None) -> model:
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.category), joinedload(cls.model.options)
            )
            .filter_by(id=model_id)
        )

        result = await session.execute(query)

        variation = result.unique().mappings().one_or_none()

        if not variation:
            raise_http_exception(VariationNotFoundException)

        return variation["Variation"]

    @classmethod
    @manage_session
    async def change(cls, variation_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        current_variation = await cls.validate_by_id(variation_id)

        if not current_variation:
            return None

        if not data:
            return current_variation

        if "category_id" in data:
            if not await ProductCategoryDAO.validate_by_id(
                data["category_id"]
            ):
                raise_http_exception(ProductCategoryNotFoundException)

        new_variation_data = get_new_data(current_variation, data)

        existing_variation = await cls.find_one_or_none(**new_variation_data)

        if existing_variation:
            raise_http_exception(VariationAlreadyExistsException)

        return await cls.update_data(variation_id, data)

    @classmethod
    @manage_session
    async def delete(cls, user, variation_id, session=None):
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Get current variation
        variation = await cls.validate_by_id(variation_id)

        if not variation:
            raise_http_exception(VariationNotFoundException)

        # Delete child variations recursively
        await cls._delete_child_variations(
            user, variation.category_id, variation.name
        )

        # Delete the variation
        await cls.delete_certain_item(variation_id)

    @classmethod
    @manage_session
    async def _delete_child_variations(
        cls, user, category_id, variation_name, session=None
    ):
        # Get child categories
        query = (
            select(ProductCategory)
            .options(joinedload(ProductCategory.children_categories))
            .filter_by(id=category_id)
        )
        result = await session.execute(query)
        category = result.scalars().unique().one_or_none()

        # Delete recursively every variation with given name
        if category and category.children_categories:
            for child_category in category.children_categories:
                current_product_category = (
                    await ProductCategoryDAO.get_product_category_variations(
                        child_category.id
                    )
                )

                if (
                    current_product_category
                    and current_product_category.variation
                ):
                    for variation in current_product_category.variation:
                        if variation.name == variation_name:
                            await cls.delete(user, variation.id)

    @classmethod
    @manage_session
    async def find_all_with_options(cls, session=None):
        query = (
            select(cls.model)
            .options(joinedload(cls.model.options))
            .order_by(cls.model.category_id)
        )

        result = await session.execute(query)

        values = result.scalars().all()

        return values
