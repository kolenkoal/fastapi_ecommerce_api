from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    VariationOptionAlreadyExistsException,
    VariationOptionNotFoundException,
    raise_http_exception,
)
from src.permissions import has_permission
from src.products.categories.models import ProductCategory
from src.utils.data_manipulation import get_new_data
from src.utils.session import manage_session
from src.variation_options.models import VariationOption
from src.variations.dao import VariationDAO
from src.variations.exceptions import VariationNotFoundException
from src.variations.models import Variation


class VariationOptionDAO(BaseDAO):
    model = VariationOption

    @classmethod
    @manage_session
    async def add(cls, user, variation_option_data, session=None):
        variation_option_data = variation_option_data.model_dump()

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        await cls._validate_variation_by_id(
            variation_option_data["variation_id"]
        )

        existing_variation_option = await cls.find_one_or_none(
            **variation_option_data
        )

        if existing_variation_option:
            raise_http_exception(VariationOptionAlreadyExistsException)

        new_variation_option = await cls._create(**variation_option_data)

        await cls._add_to_children_categories_with_options(
            variation_option_data["variation_id"], new_variation_option
        )

        return new_variation_option

    @classmethod
    @manage_session
    async def _validate_variation_by_id(cls, variation_id, session=None):
        variation = await VariationDAO.find_by_id(variation_id)

        if not variation:
            raise_http_exception(VariationNotFoundException)

    @classmethod
    @manage_session
    async def _add_to_children_categories_with_options(
        cls, variation_id, variation_option, session=None
    ):
        variation = await VariationDAO.find_one_or_none(id=variation_id)

        # Get current category
        query = (
            select(ProductCategory)
            .options(joinedload(ProductCategory.children_categories))
            .join(Variation, Variation.category_id == ProductCategory.id)
            .filter(Variation.id == variation_id)
        )
        result = await session.execute(query)
        category = result.scalars().unique().one_or_none()

        # If it exists
        if category and category.children_categories:
            # For every sub category
            for child_category in category.children_categories:
                # Check if variation exists in this category
                child_variation_data = {
                    "name": variation.name,
                    "category_id": child_category.id,
                }
                existing_variation = await VariationDAO.find_one_or_none(
                    **child_variation_data
                )
                if existing_variation:
                    # Check if such option exists
                    child_variation_option_data = {
                        "value": variation_option.value,
                        "variation_id": existing_variation.id,
                    }
                    existing_option = await cls.find_one_or_none(
                        **child_variation_option_data
                    )

                    # If it does not, create
                    if not existing_option:
                        await cls._create(**child_variation_option_data)

                    # Recursively create other
                    await cls._add_to_children_categories_with_options(
                        existing_variation.id, variation_option
                    )

    @classmethod
    @manage_session
    async def find_all(cls, session=None):
        query = select(cls.model).order_by(cls.model.value)

        result = await session.execute(query)

        values = result.scalars().all()

        return values

    @classmethod
    @manage_session
    async def find_by_id(cls, model_id, session=None) -> model:
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.variation),
            )
            .filter_by(id=model_id)
        )

        result = await session.execute(query)

        return result.unique().mappings().one_or_none()["VariationOption"]

    @classmethod
    @manage_session
    async def change(cls, variation_option_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        current_variation_option = await cls.validate_by_id(
            variation_option_id
        )

        if not current_variation_option:
            return None

        if not data:
            return current_variation_option

        if "variation_id" in data:
            if not await VariationDAO.validate_by_id(data["variation_id"]):
                raise_http_exception(VariationNotFoundException)

        new_variation_option_data = get_new_data(
            current_variation_option, data
        )

        existing_variation_option = await cls.find_one_or_none(
            **new_variation_option_data
        )

        if existing_variation_option:
            raise_http_exception(VariationOptionAlreadyExistsException)

        return await cls.update_data(variation_option_id, data)

    @classmethod
    @manage_session
    async def delete(cls, user, variation_option_id, session=None):
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Get current variation option
        variation_option = await cls.validate_by_id(variation_option_id)

        if not variation_option:
            raise_http_exception(VariationOptionNotFoundException)

        # Delete child variations recursively
        await cls._delete_child_variation_options_with_options(
            variation_option
        )

        # Delete the variation
        await cls.delete_certain_item(variation_option_id)

    @classmethod
    @manage_session
    async def _delete_child_variation_options_with_options(
        cls, variation_option, session=None
    ):
        variation = await VariationDAO.find_one_or_none(
            id=variation_option.variation_id
        )

        # Get current category
        query = (
            select(ProductCategory)
            .options(joinedload(ProductCategory.children_categories))
            .join(Variation, Variation.category_id == ProductCategory.id)
            .filter(Variation.id == variation_option.variation_id)
        )
        result = await session.execute(query)
        category = result.scalars().unique().one_or_none()

        # If the category exists and has children categories
        if category and category.children_categories:
            # For every subcategory
            for child_category in category.children_categories:
                # Check if variation exists in this category
                child_variation_data = {
                    "name": variation.name,
                    "category_id": child_category.id,
                }
                existing_variation = await VariationDAO.find_one_or_none(
                    **child_variation_data
                )

                # If variation exists, proceed with deletion
                if existing_variation:
                    # Check if such option exists
                    child_variation_option_data = {
                        "value": variation_option.value,
                        "variation_id": existing_variation.id,
                    }
                    existing_option = await cls.find_one_or_none(
                        **child_variation_option_data
                    )

                    # If the option exists, delete it
                    if existing_option:
                        # Recursively delete from other child categories
                        await cls._delete_child_variation_options_with_options(
                            existing_option
                        )

                        await cls.delete_certain_item(existing_option.id)
