from sqlalchemy import select

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    VariationAlreadyExistsException,
    VariationNotFoundException,
    raise_http_exception,
)
from src.permissions import has_permission
from src.products.categories.dao import ProductCategoryDAO
from src.utils.session import manage_session
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

        existing_variation = await cls._find_variation_by_data(variation_data)

        if existing_variation:
            raise_http_exception(VariationAlreadyExistsException)

        return await cls._create(**variation_data)

    @classmethod
    @manage_session
    async def _validate_category_by_id(cls, category_id, session=None):
        product_category = await ProductCategoryDAO.find_by_id(category_id)

        if not product_category:
            raise_http_exception(VariationNotFoundException)

    @classmethod
    @manage_session
    async def _find_variation_by_data(cls, data, session=None):
        get_variation_query = select(cls.model).filter_by(**data)

        variation = (
            await session.execute(get_variation_query)
        ).scalar_one_or_none()

        return variation
