from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    ProductItemAlreadyExistsException,
    ProductItemNotFoundException,
    raise_http_exception,
)
from src.images.router import add_product_item_image
from src.permissions import has_permission
from src.products.dao import ProductDAO
from src.products.items.models import ProductItem
from src.products.items.utils import pick
from src.users.models import User
from src.utils.session import manage_session


class ProductItemDAO(BaseDAO):
    model = ProductItem

    @classmethod
    @manage_session
    async def add(cls, user: User, data, file, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        await cls._check_product_by_id(data["product_id"])

        SKU = pick(1)

        existing_product_item = await cls.find_one_or_none(
            product_id=data["product_id"], SKU=SKU
        )

        if existing_product_item:
            raise_http_exception(ProductItemAlreadyExistsException)

        # Upload the given file to images
        uploaded_image_name = await add_product_item_image(
            SKU, data["product_id"], file
        )

        # Add product image to the data
        data.update({"product_image": uploaded_image_name, "SKU": SKU})

        return await cls._create(**data)

    @classmethod
    @manage_session
    async def _check_product_by_id(cls, product_id, session=None):
        product_item = await ProductDAO.find_by_id(product_id)

        if not product_item:
            raise_http_exception(ProductItemNotFoundException)
