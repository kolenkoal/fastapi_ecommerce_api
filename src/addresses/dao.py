from uuid import UUID

from sqlalchemy import and_, delete, desc, insert, select, update
from sqlalchemy.orm import joinedload, load_only

from src.addresses.models import Address, UserAddress
from src.addresses.schemas import SAddressOptional
from src.addresses.utils import (
    add_is_default_to_every_user_address,
    get_new_address_data,
    manage_session,
)
from src.countries.dao import CountryDAO
from src.countries.models import Country
from src.dao import BaseDAO
from src.database import superior_roles_id
from src.exceptions import (
    AddressesNotFoundException,
    AddressNotFoundException,
    CountryNotFoundException,
    DefaultAddressNotFoundException,
    ForbiddenException,
    UserAlreadyHasThisAddress,
)
from src.users.models import User


class AddressDAO(BaseDAO):
    model = Address

    @classmethod
    @manage_session
    async def add(cls, user: User, session=None, **data):
        # Check if country exists
        if not await CountryDAO.validate_country_by_id(data["country_id"]):
            raise CountryNotFoundException

        # Check if the address exists
        get_address_query = select(Address).filter_by(**data)
        address = (await session.execute(get_address_query)).scalar()

        if not address:
            # Create the address if it doesn't exist
            insert_address_query = (
                insert(cls.model).values(**data).returning(cls.model)
            )
            address = (await session.execute(insert_address_query)).scalar()

            await session.commit()

        # Check if the user already has this address added
        get_user_address_added_query = select(UserAddress.address_id).where(
            UserAddress.user_id == user.id
        )
        user_address = (
            (await session.execute(get_user_address_added_query))
            .scalars()
            .all()
        )

        if address.id in user_address:
            raise UserAlreadyHasThisAddress

        if len(user_address) > 0:
            data.update({"is_default": False})
        else:
            data.update({"is_default": True})

        # Connect user with a new address
        insert_address_query = (
            insert(UserAddress)
            .values(
                user_id=user.id,
                address_id=address.id,
                is_default=data["is_default"],
            )
            .returning(UserAddress)
        )

        await session.execute(insert_address_query)

        await session.commit()

        return address

    @classmethod
    async def _validate_country(cls, country_id):
        if not await CountryDAO.validate_country_by_id(country_id):
            raise CountryNotFoundException

    @classmethod
    async def find_all(cls, user: User):
        if user.role_id in superior_roles_id:
            return await cls._superior_user_find_all()

        return await cls._user_find_all(user)

    @classmethod
    @manage_session
    async def _user_find_all(cls, user, session=None):
        # Find all user addresses and connect it with user and country data
        get_user_addresses_data_query = (
            select(User)
            .join(UserAddress, UserAddress.user_id == User.id)
            .options(
                load_only(
                    User.email,
                    User.first_name,
                    User.last_name,
                ),
                joinedload(User.addresses)
                .joinedload(Address.country)
                .load_only(Country.id, Country.name),
            )
            .order_by(desc(UserAddress.is_default))
            .where(User.id == user.id)
        )

        # Find all user addresses
        get_user_addresses_query = select(UserAddress).where(
            UserAddress.user_id == user.id
        )

        user_addresses_data_result = await session.execute(
            get_user_addresses_data_query
        )
        user_addresses_result = await session.execute(get_user_addresses_query)

        user_address_data = (
            user_addresses_data_result.unique().mappings().one_or_none()
        )

        if not user_address_data:
            raise AddressesNotFoundException

        user_address_data = user_address_data["User"]

        return add_is_default_to_every_user_address(
            user_address_data, user_addresses_result
        )

    @classmethod
    @manage_session
    async def _superior_user_find_all(cls, session=None):
        # Find all addresses and connect it with every user and country data
        get_all_users_addresses_data_query = (
            select(User)
            .join(UserAddress, UserAddress.user_id == User.id)
            .options(
                load_only(User.email, User.first_name, User.last_name),
                joinedload(User.addresses)
                .joinedload(Address.country)
                .load_only(Country.id, Country.name),
            )
            .order_by(desc(UserAddress.is_default))
        )

        user_addresses_data_result = await session.execute(
            get_all_users_addresses_data_query
        )
        users = user_addresses_data_result.unique().mappings().all()

        if not users:
            raise AddressesNotFoundException

        users_data = []

        for user in users:
            user_data = user["User"]

            # Find all user addresses
            get_user_addresses_query = select(UserAddress).where(
                UserAddress.user_id == user_data.id
            )

            user_addresses_result = await session.execute(
                get_user_addresses_query
            )

            users_data.append(
                add_is_default_to_every_user_address(
                    user_data, user_addresses_result
                )
            )
        return {"Users": users_data}

    @classmethod
    @manage_session
    async def find_by_id(cls, user: User, address_id: UUID, session=None):
        # Get all user ids, who use this address
        get_address_users_ids_query = select(UserAddress.user_id).where(
            UserAddress.address_id == address_id
        )

        address_users_ids_result = await session.execute(
            get_address_users_ids_query
        )

        address_users_ids = address_users_ids_result.scalars().all()

        # If nobody uses this address
        if not address_users_ids:
            raise AddressNotFoundException

        # If user does not use the address or user has no permission
        if (
            user.id not in address_users_ids
            and user.role_id not in superior_roles_id
        ):
            raise ForbiddenException

        # Get and return the address
        if user.id in address_users_ids or user.role_id in superior_roles_id:
            get_address_query = (
                select(cls.model)
                .options(
                    joinedload(cls.model.country).load_only(
                        Country.id, Country.name
                    )
                )
                .where(cls.model.id == address_id)
            )

            address_result = await session.execute(get_address_query)

            address = address_result.mappings().one()["Address"]

            return address
        else:
            return None

    @classmethod
    @manage_session
    async def change_address(
        cls,
        address_id: UUID,
        user: User,
        address_data: SAddressOptional,
        session=None,
    ):
        address_data = address_data.model_dump(exclude_unset=True)

        if "country_id" in address_data:
            # If new country is not present
            if not await CountryDAO.validate_country_by_id(
                address_data["country_id"]
            ):
                raise CountryNotFoundException

        # Get all user ids, who has this address
        get_address_users_ids_query = (
            select(UserAddress.user_id)
            .select_from(UserAddress)
            .join(Address, UserAddress.address_id == Address.id)
            .where(Address.id == address_id)
        )

        address_users_ids = (
            (await session.execute(get_address_users_ids_query))
            .scalars()
            .all()
        )

        # If no one use this address
        if len(address_users_ids) < 1:
            raise AddressNotFoundException

        # If current user does not use this address
        if user.id not in address_users_ids:
            raise ForbiddenException

        get_address_query = select(cls.model).where(cls.model.id == address_id)

        current_address = (
            await session.execute(get_address_query)
        ).scalar_one_or_none()

        new_address_data = get_new_address_data(current_address, address_data)

        get_existing_address_query = select(cls.model).filter_by(
            **new_address_data
        )

        existing_address = (
            await session.execute(get_existing_address_query)
        ).scalar_one_or_none()

        if existing_address:
            if await cls._check_existing_address(existing_address, user):
                raise UserAlreadyHasThisAddress

            return await cls._update_to_existing_address(
                user, address_id, existing_address
            )

        if len(address_users_ids) == 1:
            # If only one user uses the address
            return await cls._update_to_new_address(address_data, address_id)

        else:
            # Create new address
            return await cls._create_new_address(
                new_address_data, address_id, user
            )

    @classmethod
    @manage_session
    async def _check_existing_address(
        cls, existing_address, user, session=None
    ):
        get_user_existing_address_query = select(UserAddress).where(
            and_(
                UserAddress.address_id == existing_address.id,
                UserAddress.user_id == user.id,
            )
        )

        user_existing_address_result = await session.execute(
            get_user_existing_address_query
        )

        return user_existing_address_result.scalar_one_or_none()

    @classmethod
    @manage_session
    async def set_to_default(cls, address_id: UUID, user: User, session=None):
        # Get all user ids, who use this address
        get_user_address_query = select(UserAddress).where(
            and_(
                UserAddress.address_id == address_id,
                UserAddress.user_id == user.id,
            )
        )

        user_address_result = await session.execute(get_user_address_query)

        user_address = user_address_result.scalar_one_or_none()

        if not user_address:
            raise AddressNotFoundException

        if user_address.is_default:
            return user_address

        return await cls._change_default_address(address_id, user)

    @classmethod
    @manage_session
    async def _change_default_address(
        cls, address_id: UUID, user: User, session=None
    ):
        # Get user default address
        get_default_address_query = select(UserAddress).where(
            and_(
                UserAddress.user_id == user.id,
                UserAddress.is_default == True,  # noqa
            )
        )

        default_address = (
            await session.execute(get_default_address_query)
        ).scalar()

        # If user does not have default address
        if not default_address:
            raise DefaultAddressNotFoundException

        # Set is_default to False in the default address
        unset_default_address_query = (
            update(UserAddress)
            .where(UserAddress.address_id == default_address.address_id)
            .values(is_default=False)
        )

        # Set is_default to true in the desired address
        set_default_address_query = (
            update(UserAddress)
            .where(UserAddress.address_id == address_id)
            .values(is_default=True)
            .returning(UserAddress)
        )

        await session.execute(unset_default_address_query)
        default_address_result = await session.execute(
            set_default_address_query
        )

        await session.commit()

        default_address = default_address_result.scalar()

        return default_address

    @classmethod
    @manage_session
    async def _update_to_existing_address(
        cls, user, address_id, existing_address, session=None
    ):
        update_user_address_to_existing_query = (
            update(UserAddress)
            .where(
                and_(
                    UserAddress.user_id == user.id,
                    UserAddress.address_id == address_id,
                )
            )
            .values(address_id=existing_address.id)
            .execution_options(synchronize_session=False)
        )

        await session.execute(update_user_address_to_existing_query)

        await session.commit()

        get_updated_address_query = select(Address).where(
            Address.id == existing_address.id
        )

        updated_address = (
            (await session.execute(get_updated_address_query)).scalars().one()
        )

        return updated_address

    @classmethod
    @manage_session
    async def _update_to_new_address(
        cls, address_data, address_id, session=None
    ):
        update_address_query = (
            update(Address)
            .where(Address.id == address_id)
            .values(**address_data)
            .returning(Address)
        )

        updated_address = await session.execute(update_address_query)

        await session.commit()

        return updated_address.scalars().one()

    @classmethod
    @manage_session
    async def _create_new_address(
        cls, new_address_data, address_id, user, session=None
    ):
        insert_new_address_query = (
            insert(Address).values(**new_address_data).returning(Address)
        )

        new_address = await session.execute(insert_new_address_query)

        await session.commit()

        new_address = new_address.scalars().one()

        return await cls._update_to_existing_address(
            user, address_id, new_address
        )

    @classmethod
    @manage_session
    async def _remove_user_address(cls, user, address_id, session=None):
        get_user_address_query = select(UserAddress).where(
            and_(
                UserAddress.address_id == address_id,
                UserAddress.user_id == user.id,
            )
        )

        address = (await session.execute(get_user_address_query)).scalar()

        if address.is_default:
            get_user_addresses_query = select(UserAddress).where(
                and_(
                    UserAddress.address_id != address_id,
                    UserAddress.user_id == user.id,
                )
            )

            address = (
                (await session.execute(get_user_addresses_query))
                .scalars()
                .first()
            )

            if address:
                await cls.set_to_default(address.address_id, user)

        delete_from_user_address_query = delete(UserAddress).where(
            and_(
                UserAddress.address_id == address_id,
                UserAddress.user_id == user.id,
            )
        )

        await session.execute(delete_from_user_address_query)

        await session.commit()

    @classmethod
    @manage_session
    async def _delete_certain_address(cls, user, address_id, session=None):
        if user.id not in superior_roles_id:
            await cls._remove_user_address(user, address_id)

        delete_address_query = delete(Address).where(Address.id == address_id)

        await session.execute(delete_address_query)

        await session.commit()

        return None

    @classmethod
    @manage_session
    async def delete_address(cls, user, address_id: UUID, session=None):
        get_address_users_ids_query = (
            select(UserAddress.user_id)
            .select_from(UserAddress)
            .join(Address, UserAddress.address_id == Address.id)
            .where(Address.id == address_id)
        )

        address_users_ids = (
            (await session.execute(get_address_users_ids_query))
            .scalars()
            .all()
        )

        # If no one use this address
        if len(address_users_ids) < 1:
            if user.id not in superior_roles_id:
                raise AddressNotFoundException
            return await cls._delete_certain_address(user, address_id)

        if user.id not in address_users_ids:
            raise ForbiddenException

        if len(address_users_ids) == 1:
            return await cls._delete_certain_address(user, address_id)

        else:
            return await cls._remove_user_address(user, address_id)
