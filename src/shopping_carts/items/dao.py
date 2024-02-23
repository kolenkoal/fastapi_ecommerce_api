from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dao import BaseDAO
from src.exceptions import (
    ForbiddenException,
    ProductItemNotFoundException,
    QuantityOfProductItemIsMoreThanInStockException,
    ShoppingCartItemNotFoundException,
    ShoppingCartNotFoundException,
    raise_http_exception,
)
from src.permissions import has_permission
from src.products.items.dao import ProductItemDAO
from src.products.items.models import ProductItem
from src.shopping_carts.dao import ShoppingCartDAO
from src.shopping_carts.items.models import ShoppingCartItem
from src.shopping_carts.models import ShoppingCart
from src.utils.session import manage_session


class ShoppingCartItemDAO(BaseDAO):
    model = ShoppingCartItem

    @classmethod
    @manage_session
    async def add(
        cls, shopping_cart_id, shopping_cart_item_data, user, session=None
    ):
        shopping_cart_item_data = shopping_cart_item_data.model_dump()

        user_shopping_cart = await cls._check_and_get_shopping_cart(
            shopping_cart_id, user
        )

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
            quantity = 1

            await cls.check_quantity(
                shopping_cart_item_data["product_item_id"], quantity
            )

            shopping_cart_item_data.update(
                {"cart_id": user_shopping_cart.id, "quantity": quantity}
            )
            # Create a new item in shopping cart
            return await cls._create(**shopping_cart_item_data)

        # If it exists, just add quantity
        new_quantity = existing_shopping_cart_item.quantity + 1

        await cls.check_quantity(
            shopping_cart_item_data["product_item_id"], new_quantity
        )

        return await cls.update_data(
            existing_shopping_cart_item.id,
            {"quantity": new_quantity},
        )

    @classmethod
    @manage_session
    async def check_quantity(cls, product_item_id, quantity, session=None):
        get_product_item_quantity_query = select(
            ProductItem.quantity_in_stock
        ).where(ProductItem.id == product_item_id)

        product_item_quantity = (
            await session.execute(get_product_item_quantity_query)
        ).scalar()

        if quantity > product_item_quantity:
            raise_http_exception(
                QuantityOfProductItemIsMoreThanInStockException
            )

    @classmethod
    @manage_session
    async def _check_and_get_shopping_cart(
        cls, shopping_cart_id, user, session=None
    ):
        # Get user's shopping cart
        user_shopping_cart = await ShoppingCartDAO.find_one_or_none(
            id=shopping_cart_id
        )

        # if shopping cart does not exist
        if not user_shopping_cart:
            raise_http_exception(ShoppingCartNotFoundException)

        if (
            not await has_permission(user)
            and user.id != user_shopping_cart.user_id
        ):
            raise_http_exception(ForbiddenException)

        return user_shopping_cart

    @classmethod
    @manage_session
    async def _check_product_item_exists(cls, product_item_id, session=None):
        product_item = await ProductItemDAO.find_one_or_none(
            id=product_item_id
        )

        if not product_item:
            raise_http_exception(ProductItemNotFoundException)

    @classmethod
    @manage_session
    async def find_all(cls, user, shopping_cart_id, session=None):
        # Check shopping cart exists
        await cls._check_and_get_shopping_cart(shopping_cart_id, user)

        # Get shopping cart with items
        get_shopping_carts_with_items_query = (
            select(ShoppingCart)
            .options(joinedload(ShoppingCart.cart_items))
            .where(ShoppingCart.user_id == user.id)
        )
        shopping_carts_with_items_result = await session.execute(
            get_shopping_carts_with_items_query
        )

        shopping_cart_items = (
            shopping_carts_with_items_result.unique().mappings().all()
        )

        return shopping_cart_items[0]["ShoppingCart"]

    @classmethod
    @manage_session
    async def change(
        cls, shopping_cart_id, shopping_cart_item_id, user, data, session=None
    ):
        data = data.model_dump(exclude_unset=True)

        await cls._check_and_get_shopping_cart(shopping_cart_id, user)

        current_shopping_cart_item = await cls.find_one_or_none(
            id=shopping_cart_item_id
        )

        if not current_shopping_cart_item:
            raise_http_exception(ShoppingCartItemNotFoundException)

        await cls.check_quantity(
            current_shopping_cart_item.product_item_id, data["quantity"]
        )

        return await cls.update_data(
            current_shopping_cart_item.id,
            {"quantity": data["quantity"]},
        )

    @classmethod
    @manage_session
    async def delete(
        cls, user, shopping_cart_id, shopping_cart_item_id, session=None
    ):
        await cls._check_and_get_shopping_cart(shopping_cart_id, user)

        # Get current shopping cart item
        shopping_cart_item = await cls.validate_by_id(shopping_cart_item_id)

        if not shopping_cart_item:
            raise_http_exception(ShoppingCartItemNotFoundException)

        # Delete the shopping cart item
        await cls.delete_certain_item(shopping_cart_item.id)
