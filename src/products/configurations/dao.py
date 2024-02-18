from sqlalchemy import and_, delete, insert, select

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    ProductConfigurationAlreadyExistsException,
    ProductConfigurationNotFoundException,
    ProductItemNotFoundException,
    VariationOptionNotFoundException,
    raise_http_exception,
)
from src.permissions import has_permission
from src.products.configurations.models import ProductConfiguration
from src.products.items.dao import ProductItemDAO
from src.utils.session import manage_session
from src.variation_options.dao import VariationOptionDAO


class ProductConfigurationDAO(BaseDAO):
    model = ProductConfiguration

    @classmethod
    @manage_session
    async def add(cls, user, data, session=None):
        data = data.model_dump()

        # If user is not admin
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        product_item = await ProductItemDAO.validate_by_id(
            data["product_item_id"]
        )

        if not product_item:
            raise_http_exception(ProductItemNotFoundException)

        variation_option = await VariationOptionDAO.validate_by_id(
            data["variation_option_id"]
        )

        if not variation_option:
            raise_http_exception(VariationOptionNotFoundException)

        existing_configuration = await cls.find_one_or_none(
            product_item_id=data["product_item_id"],
            variation_option_id=data["variation_option_id"],
        )

        if existing_configuration:
            raise_http_exception(ProductConfigurationAlreadyExistsException)

        return await cls._create(**data)

    @classmethod
    @manage_session
    async def find_one_or_none(cls, session=None, **filter_by) -> model:
        query = select(cls.model).filter_by(**filter_by)

        result = await session.execute(query)

        return result.scalar_one_or_none()

    @classmethod
    @manage_session
    async def find_all(cls, session=None):
        query = select(cls.model).order_by(cls.model.product_item_id)

        result = await session.execute(query)

        values = result.scalars().all()

        return values

    @classmethod
    @manage_session
    async def delete(cls, user, configuration_data, session=None):
        configuration_data = configuration_data.model_dump()
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Get current product configuration
        product_configuration = await cls.find_one_or_none(
            variation_option_id=configuration_data["variation_option_id"],
            product_item_id=configuration_data["product_item_id"],
        )

        if not product_configuration:
            raise_http_exception(ProductConfigurationNotFoundException)

        # Delete the product
        await cls.delete_product_configuration(configuration_data)

    @classmethod
    @manage_session
    async def delete_product_configuration(cls, data, session=None):
        delete_item_query = delete(cls.model).where(
            and_(
                cls.model.variation_option_id == data["variation_option_id"],
                cls.model.product_item_id == data["product_item_id"],
            )
        )

        await session.execute(delete_item_query)
        await session.commit()

        return None

    @classmethod
    @manage_session
    async def _create(cls, session=None, **data):
        create_query = insert(cls.model).values(**data).returning(cls.model)

        result = await session.execute(create_query)
        await session.commit()

        return result.scalar_one()
