import asyncio
import os
import sys

from sqlalchemy import func, select


current_file_path = os.path.abspath(__file__)

parent_dir = os.path.dirname(current_file_path)

grandparent_dir = os.path.dirname(parent_dir)

great_grandparent_dir = os.path.dirname(grandparent_dir)

sys.path.insert(1, os.path.dirname(grandparent_dir))

from src.addresses.dao import AddressDAO  # noqa
from src.addresses.models import Address, UserAddress  # noqa
from src.auth.manager import UserManager, get_user_manager  # noqa
from src.countries.models import Country  # noqa
from src.database import async_session_factory  # noqa
from src.images.router import rename_product_item_image_file  # noqa
from src.payments.methods.models import PaymentMethod  # noqa
from src.payments.types.models import PaymentType  # noqa
from src.products.categories.models import ProductCategory  # noqa
from src.products.dao import ProductDAO  # noqa
from src.products.items.models import ProductItem  # noqa
from src.products.models import Product  # noqa
from src.products.router import create_product  # noqa
from src.shopping_carts.router import create_shopping_cart  # noqa
from src.shopping_carts.schemas import SShoppingCartCreate  # noqa
from src.users.models import User  # noqa
from src.users.profiles.router import create_user_profile  # noqa
from src.users.schemas import UserCreate  # noqa
from src.utils.hasher import Hasher  # noqa
from src.utils.other_data import (  # noqa
    address_data,
    payment_methods_data,
    product_items_data,
    products_data,
    users_data,
    variation_options_data,
    variations_data,
)
from src.variations.dao import VariationDAO  # noqa
from src.variations.models import Variation  # noqa
from src.variations.options.dao import VariationOptionDAO  # noqa
from src.variations.options.models import VariationOption  # noqa
from src.variations.options.schemas import SVariationOptionCreate  # noqa
from src.variations.schemas import SVariationCreate  # noqa


async def insert_dummy_data():
    # Insert users
    async with async_session_factory() as session:
        user_query = select(User)

        users = (await session.execute(user_query)).all()

        if len(users) == 1:
            for data in users_data:
                hashed_password = Hasher.get_password_hash(
                    data["hashed_password"]
                )
                data.update({"hashed_password": hashed_password})
                created_user = User(**data)
                session.add(created_user)

                await session.commit()

                shopping_cart_data = SShoppingCartCreate(
                    user_id=created_user.id
                )
                await create_shopping_cart(shopping_cart_data, created_user)

                await create_user_profile(created_user)

    # Insert addresses
    async with async_session_factory() as session:
        user_query = select(Address)

        addresses = (await session.execute(user_query)).all()

        country_query = select(Country).filter_by(name="United States")

        country = (await session.execute(country_query)).scalar_one()

        if not addresses:
            for data in address_data:
                data.update({"country_id": country.id})
                created_address = Address(**data)
                session.add(created_address)

                await session.commit()

        # Insert user addresses
        async with async_session_factory() as session:
            variation_options_query = select(UserAddress)

            user_addresses = (
                (await session.execute(variation_options_query))
                .scalars()
                .all()
            )

            if not user_addresses:
                user_query = select(User).filter_by().offset(1)

                users = (await session.execute(user_query)).scalars().all()

                for user in users:
                    address_query = select(Address).order_by(func.random())

                    address = (await session.execute(address_query)).scalar()

                    data = {
                        "user_id": user.id,
                        "address_id": address.id,
                        "is_default": True,
                    }

                    existing_address = await AddressDAO.check_existing_address(
                        address, user
                    )

                    if not existing_address:
                        created_payment_method = UserAddress(**data)

                        session.add(created_payment_method)

                        await session.commit()

        # Insert payment methods
        async with async_session_factory() as session:
            variation_options_query = select(PaymentMethod)

            variations = (
                (await session.execute(variation_options_query))
                .scalars()
                .all()
            )

            if not variations:
                counter = 0

                user_query = select(User).filter_by().offset(1)

                users = (await session.execute(user_query)).scalars().all()

                payment_type_query = select(PaymentType)

                payment_type = (
                    await session.execute(payment_type_query)
                ).scalar_one_or_none()

                for user in users:
                    data = payment_methods_data[counter]

                    counter += 1

                    data.update(
                        {
                            "user_id": user.id,
                            "payment_type_id": payment_type.id,
                        }
                    )

                    created_payment_method = PaymentMethod(**data)

                    session.add(created_payment_method)

                    await session.commit()

        # Insert variations
        async with async_session_factory() as session:
            variation_options_query = select(Variation)

            variations = (
                (await session.execute(variation_options_query))
                .scalars()
                .all()
            )

            if not variations:
                user_query = select(User).filter_by(email="admin@admin.com")

                user = (await session.execute(user_query)).scalar_one()

                for variation in variations_data:
                    data = SVariationCreate(**variation)

                    await VariationDAO.add(user, data)

        # Insert variation options
        async with async_session_factory() as session:
            variation_options_query = select(VariationOption)

            variation_options = (
                (await session.execute(variation_options_query))
                .scalars()
                .all()
            )

            if not variation_options:
                user_query = select(User).filter_by(email="admin@admin.com")

                user = (await session.execute(user_query)).scalar_one()

                variations_query = select(Variation).filter(
                    Variation.category_id.in_((1, 2)), Variation.name == "Size"
                )

                variations = (
                    (await session.execute(variations_query)).scalars().all()
                )

                for variation in variations:
                    for variation_option in variation_options_data:
                        variation_option.update({"variation_id": variation.id})

                        data = SVariationOptionCreate(**variation_option)

                        await VariationOptionDAO.add(user, data)

                variations_query = select(Variation).filter(
                    Variation.category_id.in_((1, 2, 3)),
                    Variation.name == "Color",
                )

                variations = (
                    (await session.execute(variations_query)).scalars().all()
                )

                for variation in variations:
                    for variation_option in variation_options_data:
                        variation_option.update({"variation_id": variation.id})

                        data = SVariationOptionCreate(**variation_option)

                        await VariationOptionDAO.add(user, data)

        # Insert products
        async with async_session_factory() as session:
            product_query = select(Product)

            products = (await session.execute(product_query)).scalars().all()

            if not products:
                belt_query = select(ProductCategory.id).where(
                    ProductCategory.name == "Belts"
                )

                belt_id = (await session.execute(belt_query)).scalar_one()

                categories_query = select(ProductCategory).offset(belt_id - 1)

                categories = (
                    (await session.execute(categories_query)).scalars().all()
                )

                counter = 0

                for category in categories:
                    data = products_data[counter]
                    product_image = data["product_image"]
                    data.update({"category_id": category.id})
                    data.update(
                        {
                            "product_image": f"{product_image}_{category.id}.webp"
                        }
                    )

                    created_product = Product(**data)

                    session.add(created_product)

                    await session.commit()

                    counter += 1

        # Insert products
        async with async_session_factory() as session:
            product_items_query = select(ProductItem)

            product_items = (
                (await session.execute(product_items_query)).scalars().all()
            )

            if not product_items:
                products_query = select(Product)

                products = (
                    (await session.execute(products_query)).scalars().all()
                )

                counter = 0

                for product in products:
                    data = product_items_data[counter]
                    product_item_SKU = data["SKU"]

                    await rename_product_item_image_file(
                        old_SKU=product_item_SKU,
                        old_product="",
                        new_SKU=product_item_SKU,
                        new_product=product.id,
                    )

                    data.update(
                        {
                            "product_image": f"{product_item_SKU}_{product.id}.webp",
                            "product_id": product.id,
                        }
                    )

                    create_product_item = ProductItem(**data)

                    session.add(create_product_item)

                    await session.commit()

                    counter += 1


loop = asyncio.get_event_loop()
loop.run_until_complete(insert_dummy_data())
