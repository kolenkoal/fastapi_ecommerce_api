from datetime import date, timedelta

from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from src.addresses.dao import AddressDAO
from src.addresses.exceptions import AddressNotFoundException
from src.dao import BaseDAO
from src.exceptions import (
    ExpiredCardException,
    ForbiddenException,
    OrderStatusNotFoundException,
    ShippingMethodNotFoundException,
    ShopOrderAlreadyExistsException,
    ShopOrderNotFoundException,
    UserDoesNotHaveCartException,
    raise_http_exception,
)
from src.orders.lines.models import OrderLine
from src.orders.lines.router import create_order_line
from src.orders.lines.schemas import SOrderLineCreate
from src.orders.models import ShopOrder
from src.orders.statuses.dao import OrderStatusDAO
from src.payments.methods.dao import UserPaymentMethodDAO
from src.permissions import has_permission
from src.products.items.dao import ProductItemDAO
from src.products.items.exceptions import ProductItemNotFoundException
from src.shipping_methods.dao import ShippingMethodDAO
from src.shopping_carts.dao import ShoppingCartDAO
from src.shopping_carts.items.dao import ShoppingCartItemDAO
from src.shopping_carts.items.exceptions import (
    ShoppingCartItemsNotFoundException,
)
from src.shopping_carts.items.models import ShoppingCartItem
from src.shopping_carts.items.router import get_all_shopping_cart_items
from src.users.models import User
from src.utils.data_manipulation import get_new_data
from src.utils.session import manage_session


class ShopOrderDAO(BaseDAO):
    model = ShopOrder

    @classmethod
    @manage_session
    async def add(cls, user: User, shop_order_data, session=None):
        shop_order_data = shop_order_data.model_dump(exclude_unset=True)

        # Validate input data, the function returns the price for the shipping
        order_total = await cls._validate_input_data(user, shop_order_data)

        # Find user cart
        user_cart = await ShoppingCartDAO.find_one_or_none(user_id=user.id)

        if not user_cart:
            raise_http_exception(UserDoesNotHaveCartException)

        # Check if it is not empty
        user_cart_items = await get_all_shopping_cart_items(user_cart.id, user)

        if not user_cart_items:
            raise_http_exception(ShoppingCartItemsNotFoundException)

        # Check quantity_in_stock for every product in the cart.
        order_total = await cls._calculate_shop_order_total(
            user_cart_items, order_total
        )

        # Set order status to "Pending"
        order_status = await OrderStatusDAO.find_one_or_none(status="Pending")

        if not order_status:
            return None

        # Add data with needed values
        shop_order_data.update(
            {
                "user_id": user.id,
                "order_date": date.today(),
                "order_total": order_total,
                "order_status_id": order_status.id,
            }
        )

        # Create shop order
        shop_order = await cls._create(**shop_order_data)

        if not shop_order:
            return None

        await cls._add_every_product_to_order_line(
            user_cart_items, shop_order.id, user
        )

        await cls._clear_shopping_cart_item(user_cart.id)
        return shop_order

    @classmethod
    @manage_session
    async def _validate_input_data(cls, user, data, session=None):
        payment_method_id = data["payment_method_id"]
        shipping_address_id = data["shipping_address_id"]
        shipping_method_id = data["shipping_method_id"]

        # Find payment_method
        payment_method = await UserPaymentMethodDAO.find_payment_method(
            user, payment_method_id
        )

        # Validate the card is not expired
        if payment_method.expiry_date < date.today() + timedelta(days=1):
            raise_http_exception(ExpiredCardException)

        address = await AddressDAO.find_one_or_none(id=shipping_address_id)

        if not address:
            raise_http_exception(AddressNotFoundException)

        # Find address in user
        address_users_ids = await AddressDAO.get_address_users_ids(
            shipping_address_id
        )

        # Check if user lives on this address
        await AddressDAO.validate_existing_address(user, address_users_ids)

        # Validate shipping method exists
        shipping_method = await ShippingMethodDAO.find_one_or_none(
            id=shipping_method_id
        )

        if not shipping_method:
            raise_http_exception(ShippingMethodNotFoundException)

        return shipping_method.price

    @classmethod
    @manage_session
    async def _calculate_shop_order_total(
        cls, user_cart_items, order_total, session=None
    ):
        for item in user_cart_items.cart_items:
            await ShoppingCartItemDAO.check_quantity(
                item.product_item_id, item.quantity
            )

            product_item = await ProductItemDAO.find_one_or_none(
                id=item.product_item_id
            )

            # Add a sum for every product to order_total
            order_total += product_item.price * item.quantity

        return order_total

    @classmethod
    @manage_session
    async def _add_every_product_to_order_line(
        cls, user_cart_items, shop_order_id, user, session=None
    ):
        for item in user_cart_items.cart_items:
            product_item = await ProductItemDAO.find_one_or_none(
                id=item.product_item_id
            )

            if not product_item:
                raise_http_exception(ProductItemNotFoundException)

            order_line_data = SOrderLineCreate(
                product_item_id=item.product_item_id,
                order_id=shop_order_id,
                quantity=item.quantity,
                price=product_item.price,
            )

            new_product_item_quantity_in_stock = (
                product_item.quantity_in_stock - item.quantity
            )

            await create_order_line(shop_order_id, order_line_data, user)

            await ProductItemDAO.update_data(
                item.product_item_id,
                {"quantity_in_stock": new_product_item_quantity_in_stock},
            )

    @classmethod
    @manage_session
    async def _clear_shopping_cart_item(cls, user_cart_id, session=None):
        delete_query = delete(ShoppingCartItem).where(
            ShoppingCartItem.cart_id == user_cart_id
        )

        await session.execute(delete_query)
        await session.commit()

        return None

    @classmethod
    @manage_session
    async def find_all(cls, user, session=None):
        query = (
            select(cls.model)
            .where(cls.model.user_id == user.id)
            .order_by(cls.model.order_total)
        )

        result = await session.execute(query)

        values = result.scalars().all()

        return values

    @classmethod
    @manage_session
    async def change(cls, shop_order_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        current_shop_order = await cls.find_one_or_none(id=shop_order_id)

        if not current_shop_order:
            return None

        if not data:
            return current_shop_order

        if "order_status_id" in data:
            order_status = await OrderStatusDAO.find_one_or_none(
                id=data["order_status_id"]
            )

            if not order_status:
                raise_http_exception(OrderStatusNotFoundException)

        new_shop_order = get_new_data(current_shop_order, data)

        existing_shop_order = await cls.find_one_or_none(**new_shop_order)

        if existing_shop_order and existing_shop_order.id != shop_order_id:
            raise_http_exception(ShopOrderAlreadyExistsException)

        return await cls.update_data(shop_order_id, data)

    @classmethod
    @manage_session
    async def delete(cls, user, shop_order_id, session=None):
        # Get current order status
        shop_order = await cls.find_one_or_none(id=shop_order_id)

        if not shop_order:
            raise_http_exception(ShopOrderNotFoundException)

        if shop_order.user_id != user.id and not await has_permission(user):
            raise_http_exception(ForbiddenException)

        await cls._delete_order_lines(shop_order_id)

        # Delete the order
        await cls.delete_certain_item(shop_order_id)

    @classmethod
    @manage_session
    async def _delete_order_lines(cls, shop_order_id, session=None):
        delete_order_line_query = delete(OrderLine).where(
            OrderLine.order_id == shop_order_id
        )

        await session.execute(delete_order_line_query)
        await session.commit()

        return None

    @classmethod
    @manage_session
    async def find_shop_order_lines(cls, order_id, user, session=None):
        query = (
            select(ShopOrder)
            .options(joinedload(ShopOrder.products_in_order))
            .where(ShopOrder.id == order_id)
        )

        result = await session.execute(query)

        order = result.unique().scalars().one_or_none()

        if not order:
            raise_http_exception(ShopOrderNotFoundException)

        if order.user_id != user.id and not await has_permission(user):
            raise_http_exception(ForbiddenException)

        return order
