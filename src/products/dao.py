from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    ProductAlreadyExistsException,
    ProductCategoryNotFoundException,
    raise_http_exception,
)
from src.images.router import add_product_image
from src.permissions import has_permission
from src.products.categories.dao import ProductCategoryDAO
from src.products.models import Product
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
