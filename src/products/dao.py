from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    ProductAlreadyExistsException,
    ProductCategoryNotFoundException,
    ProductNotFoundException,
    raise_http_exception,
)
from src.images.router import (
    add_product_image,
    delete_products_file,
    rename_file,
)
from src.permissions import has_permission
from src.products.categories.dao import ProductCategoryDAO
from src.products.models import Product
from src.products.utils import get_new_product_data
from src.utils.session import manage_session


class ProductDAO(BaseDAO):
    model = Product

    @classmethod
    @manage_session
    async def add(cls, user, product_data, file, session=None):
        product_data = product_data.model_dump()

        # If user is not admin
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Validate that category exists
        await cls._validate_category_by_id(product_data["category_id"])

        # Find a product with give name and category
        # (because jeans can have same names, but be for different categories)
        existing_product = await cls.find_one_or_none(
            name=product_data["name"],
            category_id=product_data["category_id"],
        )

        if existing_product:
            raise_http_exception(ProductAlreadyExistsException)

        # Create a product image name as name and category of the product
        product_image_name = product_data["name"].lower().replace(" ", "_")

        # Upload the given file to images
        uploaded_image_name = await add_product_image(
            product_image_name, product_data["category_id"], file
        )

        # Add product image to the data
        product_data.update({"product_image": uploaded_image_name})

        # Create the product
        new_product = await cls._create(**product_data)

        return new_product

    @classmethod
    @manage_session
    async def _validate_category_by_id(cls, category_id, session=None):
        product_category = await ProductCategoryDAO.find_by_id(category_id)

        if not product_category:
            raise_http_exception(ProductCategoryNotFoundException)

    @classmethod
    @manage_session
    async def find_by_id(cls, model_id, session=None) -> model:
        query = (
            select(cls.model)
            .options(joinedload(cls.model.category))
            .filter_by(id=model_id)
        )

        result = await session.execute(query)

        product = result.unique().mappings().one_or_none()

        if not product:
            raise_http_exception(ProductNotFoundException)

        return product["Product"]

    @classmethod
    @manage_session
    async def change(cls, product_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        current_product = await cls.validate_by_id(product_id)

        if not current_product:
            return None

        if not data:
            return current_product

        if "category_id" in data:
            if not await ProductCategoryDAO.validate_by_id(
                data["category_id"]
            ):
                raise_http_exception(ProductCategoryNotFoundException)

        new_product_data = get_new_product_data(current_product, data)

        existing_product = await cls.find_one_or_none(
            name=new_product_data["name"],
            category_id=new_product_data["category_id"],
        )

        if existing_product:
            raise_http_exception(ProductAlreadyExistsException)

        new_file = await rename_file(
            old_name=current_product.name,
            old_category=current_product.category_id,
            new_name=new_product_data["name"],
            new_category=new_product_data["category_id"],
        )

        print("Newfile:", new_file)

        if new_file:
            data.update({"product_image": new_file})
            return await cls.update_data(product_id, data)

    @classmethod
    @manage_session
    async def delete(cls, user, product_id, session=None):
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Get current product
        product = await cls.validate_by_id(product_id)

        if not product:
            raise_http_exception(ProductNotFoundException)

        is_deleted = await delete_products_file(
            product.name, product.category_id
        )

        if not is_deleted:
            return None

        # Delete the product
        await cls.delete_certain_item(product_id)
