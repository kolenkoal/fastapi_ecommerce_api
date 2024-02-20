from src.dao import BaseDAO
from src.exceptions import (
    ProductItemNotFoundException,
    ShoppingCartNotFoundException,
    raise_http_exception,
)
from src.products.items.dao import ProductItemDAO
from src.shopping_carts.dao import ShoppingCartDAO
from src.shopping_carts.items.models import ShoppingCartItem
from src.utils.session import manage_session


class ShoppingCartItemDAO(BaseDAO):
    model = ShoppingCartItem

    @classmethod
    @manage_session
    async def add(cls, shopping_cart_item_data, user, session=None):
        shopping_cart_item_data = shopping_cart_item_data.model_dump()

        # Get user's shopping cart
        user_shopping_cart = await ShoppingCartDAO.find_one_or_none(
            user_id=user.id
        )

        # if shopping cart does not exist
        if not user_shopping_cart:
            raise_http_exception(ShoppingCartNotFoundException)

        # Check if product item exists
        await cls._check_product_item_exists(
            shopping_cart_item_data["product_item_id"]
        )

        # Get existing item in some shopping cart
        existing_shopping_cart_item = (
            await ShoppingCartItemDAO.find_one_or_none(
                cart_id=user_shopping_cart.id,
                product_item_id=shopping_cart_item_data["product_item_id"],
            )
        )

        # If it does not exist
        if not existing_shopping_cart_item:
            shopping_cart_item_data.update(
                {"cart_id": user_shopping_cart.id, "quantity": 1}
            )
            # Create a new item in shopping cart
            return await cls._create(**shopping_cart_item_data)

        # If it exists, just add quantity
        return await cls.update_data(
            existing_shopping_cart_item.id,
            {"quantity": existing_shopping_cart_item.quantity + 1},
        )

    @classmethod
    @manage_session
    async def _check_product_item_exists(cls, product_item_id, session=None):
        product_item = await ProductItemDAO.find_one_or_none(
            id=product_item_id
        )

        if not product_item:
            raise_http_exception(ProductItemNotFoundException)
