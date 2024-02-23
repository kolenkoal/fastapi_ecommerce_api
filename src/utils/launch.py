import asyncio
import os
import sys

from sqlalchemy import select


current_file_path = os.path.abspath(__file__)

parent_dir = os.path.dirname(current_file_path)

grandparent_dir = os.path.dirname(parent_dir)

great_grandparent_dir = os.path.dirname(grandparent_dir)

sys.path.insert(1, os.path.dirname(grandparent_dir))

from src.config import settings  # noqa
from src.countries.models import Country  # noqa
from src.database import async_session_factory  # noqa
from src.orders.statuses.models import OrderStatus  # noqa
from src.payments.payment_types.models import PaymentType  # noqa
from src.products.categories.models import ProductCategory  # noqa
from src.shipping_methods.models import ShippingMethod  # noqa
from src.users.models import Role, User  # noqa
from src.utils.data import (  # noqa
    admin_data,
    countries_data,
    order_statuses_data,
    payment_types_data,
    product_categories_data,
    product_sub_categories_data,
    product_sub_sub_categories_data,
    roles_data,
    shipping_methods_data,
)
from src.utils.hasher import Hasher  # noqa


async def insert_initial_values():
    async with async_session_factory() as session:
        query = select(Role).filter_by(name="user")

        result = await session.execute(query)

        role = result.all()

        if not role:
            for data in roles_data:
                role = Role(**data)
                session.add(role)

            await session.commit()

    async with async_session_factory() as session:
        hashed_password = Hasher.get_password_hash(
            admin_data["hashed_password"]
        )

        admin_data.update({"hashed_password": hashed_password})

        query = select(User).filter_by(email="admin@admin.com")

        result = await session.execute(query)

        admin = result.all()

        if not admin:
            admin = User(**admin_data)
            session.add(admin)

            await session.commit()

    async with async_session_factory() as session:
        query = select(Country)

        result = await session.execute(query)

        country = result.all()

        if not country:
            for data in countries_data:
                country = Country(**data)
                session.add(country)

            await session.commit()

    async with async_session_factory() as session:
        query = select(PaymentType)

        result = await session.execute(query)

        payment_types = result.all()

        if not payment_types:
            for data in payment_types_data:
                payment_type = PaymentType(**data)
                session.add(payment_type)

            await session.commit()

    async with async_session_factory() as session:
        query = select(ProductCategory)

        result = await session.execute(query)

        product_categories = result.all()

        if not product_categories:
            for data in product_categories_data:
                product_category = ProductCategory(**data)
                session.add(product_category)
                await session.commit()

            for data in product_sub_categories_data:
                product_category = ProductCategory(**data)
                session.add(product_category)
                await session.commit()

            for data in product_sub_sub_categories_data:
                product_category = ProductCategory(**data)
                session.add(product_category)
                await session.commit()

        async with async_session_factory() as session:
            query = select(ShippingMethod).filter_by(name="Standard")

            result = await session.execute(query)

            shipping_method = result.one_or_none()

            if not shipping_method:
                for data in shipping_methods_data:
                    shipping_method = ShippingMethod(**data)
                    session.add(shipping_method)

                await session.commit()

        async with async_session_factory() as session:
            query = select(OrderStatus).filter_by(status="Pending")

            result = await session.execute(query)

            order_status = result.one_or_none()

            if not order_status:
                for data in order_statuses_data:
                    order_status = OrderStatus(**data)
                    session.add(order_status)

                await session.commit()


loop = asyncio.get_event_loop()
loop.run_until_complete(insert_initial_values())
