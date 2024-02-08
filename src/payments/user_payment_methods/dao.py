from datetime import date, timedelta

from sqlalchemy import and_, desc, select, update
from sqlalchemy.orm import joinedload, load_only

from src.dao import BaseDAO
from src.database import superior_roles_id
from src.exceptions import (
    CardAlreadyConnectedWithOtherUserException,
    ExpiredCardException,
    ForbiddenException,
    PaymentMethodAlreadyExists,
    PaymentMethodNotFoundException,
    PaymentMethodsNotFoundException,
    PaymentTypeNotFoundException,
    raise_http_exception,
)
from src.payments.payment_types.models import PaymentType
from src.payments.user_payment_methods.models import UserPaymentMethod
from src.payments.user_payment_methods.utils import get_new_payment_method_data
from src.users.models import User
from src.utils.session import manage_session


class UserPaymentMethodDAO(BaseDAO):
    model = UserPaymentMethod

    @classmethod
    @manage_session
    async def add_payment_method(cls, user: User, session=None, **data):
        await cls._validate_payment_type_id(data["payment_type_id"])

        data.update({"user_id": user.id})

        await cls._check_payment_method(user, data["account_number"])

        user_payment_methods = await cls._find_payment_methods(user)

        if not user_payment_methods:
            data.update({"is_default": True})

        payment_method = await cls.insert(**data)

        if user_payment_methods:
            if data["is_default"]:
                await cls.set_default(user, payment_method.id)

        return payment_method

    @classmethod
    @manage_session
    async def _check_payment_method(
        cls, user, payment_method_account_number, session=None
    ):
        get_payment_method_query = select(UserPaymentMethod).where(
            UserPaymentMethod.account_number == payment_method_account_number
        )
        payment_method = (
            await session.execute(get_payment_method_query)
        ).scalar_one_or_none()

        if payment_method:
            if payment_method.user_id != user.id:
                raise_http_exception(
                    CardAlreadyConnectedWithOtherUserException
                )
            raise_http_exception(PaymentMethodAlreadyExists)

    @classmethod
    @manage_session
    async def _validate_payment_type_id(cls, payment_type_id, session=None):
        get_payment_type_query = select(PaymentType).where(
            PaymentType.id == payment_type_id
        )
        payment_type = (
            await session.execute(get_payment_type_query)
        ).scalar_one_or_none()

        if not payment_type:
            raise_http_exception(PaymentTypeNotFoundException)

        return payment_type

    @classmethod
    @manage_session
    async def _find_payment_methods(cls, user, session=None):
        get_user_payment_methods_query = select(UserPaymentMethod).where(
            UserPaymentMethod.user_id == user.id
        )
        user_payment_methods = (
            (await session.execute(get_user_payment_methods_query))
            .scalars()
            .all()
        )

        if not user_payment_methods:
            return None

        return user_payment_methods

    @classmethod
    async def find_all(cls, user: User):
        if user.role_id in superior_roles_id:
            return await cls._superior_user_find_all(user)

        return await cls._user_find_all(user)

    @classmethod
    @manage_session
    async def _user_find_all(cls, user, session=None):
        user_payment_method_data = (
            await cls._get_user_payment_methods_and_payment_types_data(user)
        )

        if not user_payment_method_data:
            raise_http_exception(PaymentMethodsNotFoundException)

        return user_payment_method_data[0]["User"]

    @classmethod
    @manage_session
    async def _superior_user_find_all(cls, user, session=None):
        users_payment_method_data = (
            await cls._get_user_payment_methods_and_payment_types_data(user)
        )

        if not users_payment_method_data:
            raise_http_exception(PaymentMethodsNotFoundException)

        users_data = []

        for user in users_payment_method_data:
            user_data = user["User"]

            users_data.append(user_data)

        return {"Users": users_data}

    @classmethod
    @manage_session
    async def _get_user_payment_methods_and_payment_types_data(
        cls, user, session=None
    ):
        get_user_payment_methods_data_query = (
            select(User)
            .join(UserPaymentMethod, User.id == UserPaymentMethod.user_id)
            .options(
                load_only(
                    User.email,
                    User.first_name,
                    User.last_name,
                ),
                joinedload(User.payment_methods).joinedload(
                    UserPaymentMethod.payment_type
                ),
            )
            .order_by(desc(UserPaymentMethod.is_default))
        )

        if user.role_id not in superior_roles_id:
            get_user_payment_methods_data_query = (
                get_user_payment_methods_data_query.where(User.id == user.id)
            )

        user_payment_methods_data_result = await session.execute(
            get_user_payment_methods_data_query
        )

        user_payment_method_data = (
            user_payment_methods_data_result.unique().mappings().all()
        )

        return user_payment_method_data

    @classmethod
    @manage_session
    async def set_default(
        cls, user, new_default_payment_method_id, session=None
    ):
        default_payment_method = await cls._find_default_payment_method(
            user, new_default_payment_method_id
        )

        return await cls._switch_default_payment_method(
            default_payment_method, new_default_payment_method_id
        )

    @classmethod
    @manage_session
    async def _find_default_payment_method(
        cls, user, new_default_payment_method_id, session=None
    ):
        get_default_payment_method_query = select(UserPaymentMethod).where(
            and_(
                UserPaymentMethod.user_id == user.id,
                UserPaymentMethod.id != new_default_payment_method_id,
                UserPaymentMethod.is_default == True,  # noqa
            )
        )

        default_payment_method = (
            await session.execute(get_default_payment_method_query)
        ).scalar()

        return default_payment_method

    @classmethod
    @manage_session
    async def _switch_default_payment_method(
        cls,
        default_payment_method,
        new_default_payment_method_id,
        session=None,
    ):
        unset_default_payment_method_query = (
            update(UserPaymentMethod)
            .where(UserPaymentMethod.id == default_payment_method.id)
            .values(is_default=False)
        )

        set_default_payment_method_query = (
            update(UserPaymentMethod)
            .where(UserPaymentMethod.id == new_default_payment_method_id)
            .values(is_default=True)
            .returning(UserPaymentMethod)
        )

        await session.execute(unset_default_payment_method_query)
        default_payment_method_result = await session.execute(
            set_default_payment_method_query
        )

        await session.commit()

        default_payment_method = default_payment_method_result.scalar()

        return default_payment_method

    @classmethod
    @manage_session
    async def find_payment_method(cls, user, payment_method_id, session=None):
        payment_method = await cls._find_by_id(payment_method_id)

        if not payment_method:
            raise_http_exception(PaymentMethodNotFoundException)

        if (
            payment_method.user_id != user.id
            and user.id not in superior_roles_id
        ):
            raise_http_exception(ForbiddenException)

        return payment_method

    @classmethod
    @manage_session
    async def _find_by_id(cls, payment_method_id, session=None):
        get_payment_method_query = select(UserPaymentMethod).where(
            UserPaymentMethod.id == payment_method_id
        )

        payment_method_result = await session.execute(get_payment_method_query)

        payment_method = payment_method_result.scalar_one_or_none()

        return payment_method

    @classmethod
    @manage_session
    async def change_payment_method(
        cls, payment_method_id, user, payment_method_data, session=None
    ):
        payment_method_data = payment_method_data.model_dump(
            exclude_unset=True
        )

        current_payment_method = await cls._find_by_id(payment_method_id)

        if not current_payment_method:
            raise_http_exception(PaymentMethodNotFoundException)

        if (
            current_payment_method.user_id != user.id
            and user.id not in superior_roles_id
        ):
            raise_http_exception(ForbiddenException)

        new_payment_method_data = get_new_payment_method_data(
            current_payment_method, payment_method_data
        )

        if new_payment_method_data["expiry_date"] < date.today() + timedelta(
            days=1
        ):
            raise_http_exception(ExpiredCardException)

        existing_payment_method = await cls._get_existing_payment_method(
            new_payment_method_data
        )

        return await cls._handle_existing_or_new_payment_method(
            existing_payment_method,
            user,
            payment_method_id,
            new_payment_method_data,
        )

    @classmethod
    @manage_session
    async def _get_existing_payment_method(
        cls, new_payment_method_data, session=None
    ):
        get_existing_payment_method_query = select(cls.model).filter_by(
            **new_payment_method_data
        )

        existing_payment_method = (
            await session.execute(get_existing_payment_method_query)
        ).scalar_one_or_none()

        return existing_payment_method

    @classmethod
    @manage_session
    async def _handle_existing_or_new_payment_method(
        cls,
        existing_payment_method,
        user,
        payment_method_id,
        new_payment_method_data,
        session=None,
    ):
        if existing_payment_method:
            if existing_payment_method.user_id == user.id:
                raise_http_exception(PaymentMethodAlreadyExists)
            raise_http_exception(ForbiddenException)

        return await cls._update_payment_method(
            new_payment_method_data, payment_method_id
        )

    @classmethod
    @manage_session
    async def _find_user_default_payment_method(cls, user, session=None):
        get_default_user_payment_method_query = select(
            UserPaymentMethod
        ).where(
            and_(
                UserPaymentMethod.user_id == user.id,
                UserPaymentMethod.is_default == True,  # noqa
            )
        )
        user_default_payment_method = (
            await session.execute(get_default_user_payment_method_query)
        ).scalar_one_or_none()

        if not user_default_payment_method:
            return None

        return user_default_payment_method

    @classmethod
    @manage_session
    async def _update_payment_method(
        cls, payment_method_data, payment_method_id, session=None
    ):
        update_payment_method_query = (
            update(UserPaymentMethod)
            .where(UserPaymentMethod.id == payment_method_id)
            .values(**payment_method_data)
            .returning(UserPaymentMethod)
        )

        updated_payment_method = await session.execute(
            update_payment_method_query
        )
        await session.commit()

        return updated_payment_method.scalars().one()
