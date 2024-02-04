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
        try:
            await cls._validate_country(data["country_id"])
            address = await cls._get_or_create_address(session, **data)
            await cls._check_and_insert_user_address(session, user, address)
            return address
        except CountryNotFoundException:
            print("Country not found.")
        except UserAlreadyHasThisAddress:
            print("User already has this address.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    async def _validate_country(cls, country_id):
        try:
            if not await CountryDAO.validate_country_by_id(country_id):
                raise CountryNotFoundException
        except CountryNotFoundException:
            print("Country not found.")

    @classmethod
    async def _get_or_create_address(cls, session, **data):
        try:
            get_address_query = select(cls.model).filter_by(**data)
            address = (await session.execute(get_address_query)).scalar()

            if not address:
                insert_address_query = (
                    insert(cls.model).values(**data).returning(cls.model)
                )
                address = (
                    await session.execute(insert_address_query)
                ).scalar()
                await session.commit()

            return address
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    async def _check_and_insert_user_address(cls, session, user, address):
        try:
            user_address_ids_query = select(UserAddress.address_id).where(
                UserAddress.user_id == user.id
            )
            user_address_ids = (
                (await session.execute(user_address_ids_query)).scalars().all()
            )

            if address.id in user_address_ids:
                raise UserAlreadyHasThisAddress

            data = {
                "user_id": user.id,
                "address_id": address.id,
                "is_default": not bool(user_address_ids),
            }

            insert_user_address_query = (
                insert(UserAddress).values(**data).returning(UserAddress)
            )

            await session.execute(insert_user_address_query)
            await session.commit()
        except UserAlreadyHasThisAddress:
            print("User already has this address.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    async def find_all(cls, user: User):
        try:
            if user.role_id in superior_roles_id:
                return await cls._superior_user_find_all()

            return await cls._user_find_all(user)
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _user_find_all(cls, user, session=None):
        try:
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

            get_user_addresses_query = select(UserAddress).where(
                UserAddress.user_id == user.id
            )

            user_addresses_data_result = await session.execute(
                get_user_addresses_data_query
            )
            user_addresses_result = await session.execute(
                get_user_addresses_query
            )

            user_address_data = (
                user_addresses_data_result.unique().mappings().one_or_none()
            )

            if not user_address_data:
                raise AddressesNotFoundException

            user_address_data = user_address_data["User"]

            return add_is_default_to_every_user_address(
                user_address_data, user_addresses_result
            )
        except AddressesNotFoundException:
            print("Addresses not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _superior_user_find_all(cls, session=None):
        try:
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
        except AddressesNotFoundException:
            print("Addresses not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def find_by_id(cls, user: User, address_id: UUID, session=None):
        try:
            get_address_users_ids_query = select(UserAddress.user_id).where(
                UserAddress.address_id == address_id
            )

            address_users_ids = (
                (await session.execute(get_address_users_ids_query))
                .scalars()
                .all()
            )

            if not address_users_ids:
                raise AddressNotFoundException

            if (
                user.id not in address_users_ids
                and user.role_id not in superior_roles_id
            ):
                raise ForbiddenException

            if (
                user.id in address_users_ids
                or user.role_id in superior_roles_id
            ):
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
        except AddressNotFoundException:
            print("Address not found.")
        except ForbiddenException:
            print("Forbidden access.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def change_address(
        cls,
        address_id: UUID,
        user: User,
        address_data: SAddressOptional,
        session=None,
    ):
        try:
            address_data = address_data.model_dump(exclude_unset=True)
            await cls._validate_new_country(address_data)

            address_users_ids = await cls._get_address_users_ids(address_id)
            await cls._validate_existing_address(user, address_users_ids)

            current_address = await cls._get_current_address(address_id)

            new_address_data = get_new_address_data(
                current_address, address_data
            )

            existing_address = await cls._get_existing_address(
                new_address_data
            )

            return await cls._handle_existing_or_new_address(
                existing_address,
                user,
                address_id,
                new_address_data,
                address_users_ids,
            )
        except CountryNotFoundException:
            print("Country not found.")
        except UserAlreadyHasThisAddress:
            print("User already has this address.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    async def _validate_new_country(cls, address_data):
        try:
            if "country_id" in address_data:
                if not await CountryDAO.validate_country_by_id(
                    address_data["country_id"]
                ):
                    raise CountryNotFoundException
        except CountryNotFoundException:
            print("Country not found.")

    @classmethod
    @manage_session
    async def _validate_existing_address(
        cls, user, address_users_ids, session=None
    ):  # Fixed
        try:
            if (
                user.id not in address_users_ids
                and user.role_id not in superior_roles_id
            ):
                raise ForbiddenException
        except ForbiddenException:
            print("Forbidden access.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _get_current_address(cls, address_id, session=None):
        try:
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

            address = address_result.scalars().one_or_none()

            return address
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _get_existing_address(
        cls, new_address_data, session=None
    ):  # Fixed
        try:
            get_existing_address_query = select(cls.model).filter_by(
                **new_address_data
            )

            existing_address = (
                await session.execute(get_existing_address_query)
            ).scalar_one_or_none()

            return existing_address
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _get_address_users_ids(cls, address_id: UUID, session=None):
        try:
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

            return address_users_ids
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _handle_existing_or_new_address(
        cls,
        existing_address,
        user,
        address_id,
        new_address_data,
        address_users_ids,
        session=None,
    ):
        try:
            if existing_address:
                if await cls._check_existing_address(existing_address, user):
                    raise UserAlreadyHasThisAddress
                return await cls._update_to_existing_address(
                    user, address_id, existing_address, session
                )

            if len(address_users_ids) == 1:
                return await cls._update_to_new_address(
                    new_address_data, address_id
                )
            else:
                return await cls._create_new_address(
                    new_address_data, address_id, user, session
                )
        except UserAlreadyHasThisAddress:
            print("User already has this address.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _check_existing_address(
        cls, existing_address, user, session=None
    ):
        try:
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
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def set_to_default(cls, address_id: UUID, user: User, session=None):
        try:
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
        except AddressNotFoundException:
            print("Address not found.")
        except DefaultAddressNotFoundException:
            print("Default address not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _change_default_address(
        cls, address_id: UUID, user: User, session=None
    ):
        try:
            get_default_address_query = select(UserAddress).where(
                and_(
                    UserAddress.user_id == user.id,
                    UserAddress.is_default == True,  # noqa
                )
            )

            default_address = (
                await session.execute(get_default_address_query)
            ).scalar()

            if not default_address:
                raise DefaultAddressNotFoundException

            unset_default_address_query = (
                update(UserAddress)
                .where(UserAddress.address_id == default_address.address_id)
                .values(is_default=False)
            )

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
        except DefaultAddressNotFoundException:
            print("Default address not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _update_to_existing_address(
        cls, user, address_id, existing_address, session=None
    ):
        try:
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
                (await session.execute(get_updated_address_query))
                .scalars()
                .one()
            )

            return updated_address
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _update_to_new_address(
        cls, address_data, address_id, session=None
    ):
        try:
            update_address_query = (
                update(Address)
                .where(Address.id == address_id)
                .values(**address_data)
                .returning(Address)
            )

            updated_address = await session.execute(update_address_query)
            await session.commit()

            return updated_address.scalars().one()
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _create_new_address(
        cls, new_address_data, address_id, user, session=None
    ):
        try:
            insert_new_address_query = (
                insert(Address).values(**new_address_data).returning(Address)
            )

            new_address = await session.execute(insert_new_address_query)
            await session.commit()

            new_address = new_address.scalars().one()

            return await cls._update_to_existing_address(
                user, address_id, new_address, session
            )
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _remove_user_address(cls, user, address_id, session=None):
        try:
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
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def _delete_certain_address(cls, user, address_id, session=None):
        try:
            if user.id not in superior_roles_id:
                await cls._remove_user_address(user, address_id)

            delete_address_query = delete(Address).where(
                Address.id == address_id
            )

            await session.execute(delete_address_query)
            await session.commit()

            return None
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    @manage_session
    async def delete_address(cls, user, address_id: UUID, session=None):
        try:
            address_users_ids = await cls._get_address_users_ids(address_id)

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
        except AddressNotFoundException:
            print("Address not found.")
        except ForbiddenException:
            print("Forbidden access.")
        except Exception as e:
            print(f"An error occurred: {e}")
