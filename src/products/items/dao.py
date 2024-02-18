from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    ProductItemNotFoundException,
    ProductNotFoundException,
    raise_http_exception,
)
from src.images.router import (
    add_product_item_image,
    delete_product_item_file,
    rename_product_item_image_file,
)
from src.permissions import has_permission
from src.products.dao import ProductDAO
from src.products.items.models import ProductItem
from src.products.items.utils import pick
from src.users.models import User
from src.utils.data_manipulation import get_new_data
from src.utils.session import manage_session


class ProductItemDAO(BaseDAO):
    model = ProductItem

    @classmethod
    @manage_session
    async def add(cls, user: User, data, file, session=None):
        data = data.model_dump(exclude_unset=True)

        # If user is not admin
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Validate that product exists
        await cls._check_product_by_id(data["product_id"])

        # Generate SKU for the product item
        SKU = pick(1)

        # Upload the given file to images
        uploaded_image_name = await add_product_item_image(
            SKU, data["product_id"], file
        )

        # Add product image to the data
        data.update({"product_image": uploaded_image_name, "SKU": SKU})

        # Create the product item
        return await cls._create(**data)

    @classmethod
    @manage_session
    async def _check_product_by_id(cls, product_id, session=None):
        product_item = await ProductDAO.find_by_id(product_id)

        if not product_item:
            raise_http_exception(ProductItemNotFoundException)

    @classmethod
    @manage_session
    async def find_all(cls, session=None):
        query = select(cls.model).order_by(cls.model.price)

        result = await session.execute(query)

        values = result.scalars().all()

        return values

    @classmethod
    @manage_session
    async def find_by_id(cls, model_id, session=None) -> model:
        query = (
            select(cls.model)
            .options(joinedload(cls.model.product))
            .filter_by(id=model_id)
        )

        result = await session.execute(query)

        product_item = result.unique().mappings().one_or_none()

        if not product_item:
            raise_http_exception(ProductItemNotFoundException)

        return product_item["ProductItem"]

    @classmethod
    @manage_session
    async def change(cls, product_item_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        current_product_item = await cls.validate_by_id(product_item_id)

        if not current_product_item:
            return None

        if not data:
            return current_product_item

        if "product_id" in data:
            if not await ProductDAO.validate_by_id(data["product_id"]):
                raise_http_exception(ProductNotFoundException)

        new_product_item_data = get_new_data(current_product_item, data)

        new_file = await rename_product_item_image_file(
            old_SKU=current_product_item.SKU,
            old_product=current_product_item.product_id,
            new_SKU=new_product_item_data["SKU"],
            new_product=new_product_item_data["product_id"],
        )

        if new_file:
            data.update({"product_image": new_file})

        return await cls.update_data(product_item_id, data)

    @classmethod
    @manage_session
    async def delete(cls, user, product_item_id, session=None):
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Get current product item
        product_item = await cls.validate_by_id(product_item_id)

        if not product_item:
            raise_http_exception(ProductItemNotFoundException)

        is_deleted = await delete_product_item_file(
            product_item.SKU, product_item.product_id
        )

        if not is_deleted:
            return None

        # Delete the product item
        await cls.delete_certain_item(product_item_id)

    @classmethod
    @manage_session
    async def get_product_item_configurations(
        cls, product_item_id: UUID, session=None
    ):
        query = (
            select(cls.model)
            .options(joinedload(cls.model.variations))
            .filter_by(id=product_item_id)
        )

        result = await session.execute(query)

        product_item_configurations = (
            result.unique().mappings().one_or_none()["ProductItem"]
        )

        return product_item_configurations
