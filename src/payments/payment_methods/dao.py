from datetime import date, timedelta

from sqlalchemy import and_, delete, desc, select, update
from sqlalchemy.orm import joinedload, load_only

from src.dao import BaseDAO
from src.database import superior_roles_id
from src.exceptions import (
    ExpiredCardException,
    ForbiddenException,
    PaymentMethodAlreadyExists,
    PaymentMethodNotFoundException,
    PaymentMethodsNotFoundException,
    PaymentTypeNotFoundException,
    raise_http_exception,
)
from src.payments.payment_methods.models import UserPaymentMethod
from src.payments.payment_methods.utils import get_new_payment_method_data
from src.payments.payment_types.models import PaymentType
from src.users.models import User
from src.utils.session import manage_session


class UserPaymentMethodDAO(BaseDAO):
    model = UserPaymentMethod

    @classmethod
    @manage_session
    async def add_payment_method(cls, user: User, session=None, **data):
        """
        Adds a payment method to the system.

        Args:
            user (User): The user adding the payment method.
            session (Session, optional): The database session.
            **data: Additional data for the payment method.

        Returns:
            UserPaymentMethod: The newly created payment method.
        """

        # Make sure payment type exists
        await cls._validate_payment_type_id(data["payment_type_id"])

        # Add user_id to the method.
        data.update({"user_id": user.id})

        # Verify card does not belong to any other user
        await cls._check_payment_method(user, data["account_number"])

        # Get user payment methods
        user_payment_methods = await cls._find_payment_method(user)

        # If user doesn't have payment methods, the new one should be default
        if not user_payment_methods:
            data.update({"is_default": True})

        # Add payment method to the database.
        payment_method = await cls.insert(**data)

        # If user wants a new payment method to be default, make it default
        if user_payment_methods:
            if "is_default" in data and data["is_default"]:
                await cls.set_default(user, payment_method.id)

        return payment_method

    @classmethod
    @manage_session
    async def _check_payment_method(
        cls, user, payment_method_account_number, session=None
    ):
        """
        Checks if the provided payment method already exists in the system.

        Args:
            user: The user associated with the payment method.
            payment_method_account_number: The account number of the payment method.
            session (Session, optional): The database session.

        Raises:
            ForbiddenException: If the payment method belongs to another user.
            PaymentMethodAlreadyExists: If the payment method already exists in the system.
        """
        get_payment_method_query = select(cls.model).where(
            cls.model.account_number == payment_method_account_number
        )
        payment_method = (
            await session.execute(get_payment_method_query)
        ).scalar_one_or_none()

        if payment_method:
            if payment_method.user_id != user.id:
                raise_http_exception(ForbiddenException)
            raise_http_exception(PaymentMethodAlreadyExists)

    @classmethod
    @manage_session
    async def _validate_payment_type_id(cls, payment_type_id, session=None):
        """
        Validates if the given payment type exists.

        Args:
            payment_type_id: The ID of the payment type.
            session (Session, optional): The database session.

        Returns:
            PaymentType: The payment type if found.

        Raises:
            PaymentTypeNotFoundException: If the payment type doesn't exist.
        """
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
    async def _find_payment_method(cls, user, session=None):
        """
        Finds payment methods associated with the given user.

        Args:
            user: The user whose payment methods are to be found.
            session (Session, optional): The database session.

        Returns:
            UserPaymentMethod: The user's payment method if found, else None
        """
        get_user_payment_methods_query = select(cls.model).where(
            cls.model.user_id == user.id
        )
        user_payment_methods = (
            (await session.execute(get_user_payment_methods_query))
            .scalars()
            .first()
        )

        if not user_payment_methods:
            return None

        return user_payment_methods

    @classmethod
    async def find_all(cls, user: User):
        """
        Finds all payment methods associated with the given user.

        Args:
            user: The user whose payment methods are to be found.

        Returns:
            dict: A dictionary containing user's payment methods.

        Raises:
            PaymentMethodsNotFoundException: If no payment methods are
            found for the user.
        """

        if user.role_id in superior_roles_id:
            return await cls._superior_user_find_all(user)

        return await cls._user_find_all(user)

    @classmethod
    @manage_session
    async def _user_find_all(cls, user, session=None):
        """
        Finds all payment methods associated with the given user.

        Args:
            user: The user whose payment methods are to be found.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            dict: A dictionary containing user's payment methods.

        Raises:
            PaymentMethodsNotFoundException: If no payment methods are found for the user.
        """

        # Merge user with his payment methods and payment types
        user_payment_method_data = (
            await cls._get_user_payment_methods_and_payment_types_data(user)
        )

        if not user_payment_method_data:
            raise_http_exception(PaymentMethodsNotFoundException)

        return user_payment_method_data[0]["User"]

    @classmethod
    @manage_session
    async def _superior_user_find_all(cls, user, session=None):
        """
        Finds all payment methods associated with the given user and all subordinate users.

        Args:
            user: The user whose payment methods are to be found.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            dict: A dictionary containing payment methods for user and their subordinates.

        Raises:
            PaymentMethodsNotFoundException: If no payment methods are found for the users.
        """
        # Merge users with their payment methods and payment types
        users_payment_method_data = (
            await cls._get_user_payment_methods_and_payment_types_data(user)
        )

        if not users_payment_method_data:
            raise_http_exception(PaymentMethodsNotFoundException)

        # Remove extra arrays
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
        """
        Retrieves data about user's payment methods along with associated payment types.

        Args:
            user: The user whose payment methods data is to be retrieved.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            list: A list of dictionaries containing payment methods data.

        Raises:
            PaymentMethodsNotFoundException: If no payment methods are found for the user.
        """
        get_user_payment_methods_data_query = (
            select(User)
            .join(cls.model, User.id == cls.model.user_id)
            .options(
                load_only(
                    User.email,
                    User.first_name,
                    User.last_name,
                ),
                joinedload(User.payment_methods).joinedload(
                    cls.model.payment_type
                ),
            )
            .order_by(desc(cls.model.is_default))
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
        """
        Sets the default payment method for the user.

        Args:
            user: The user for whom the default payment method is to be set.
            new_default_payment_method_id: The ID of the new default payment method.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            UserPaymentMethod: The updated default payment method.

        Raises:
            ForbiddenException: If the user does not have permission to set the default payment method.
        """
        # Get default payment method
        default_payment_method = await cls._find_default_payment_method(
            user, new_default_payment_method_id
        )

        # Switch id_default in current default and new payment methods
        return await cls._switch_default_payment_method(
            default_payment_method, new_default_payment_method_id
        )

    @classmethod
    @manage_session
    async def _find_default_payment_method(
        cls, user, new_default_payment_method_id, session=None
    ):
        """
        Finds the current default payment method for the user.

        Args:
            user: The user whose default payment method is to be found.
            new_default_payment_method_id: The ID of the new default payment method.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            UserPaymentMethod: The current default payment method.

        Raises:
            ForbiddenException: If the user does not have permission to set the default payment method.
        """
        get_default_payment_method_query = select(cls.model).where(
            and_(
                cls.model.user_id == user.id,
                cls.model.id != new_default_payment_method_id,
                cls.model.is_default == True,  # noqa
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
        """
        Switches the default payment method for the user.

        Args:
            default_payment_method: The current default payment method.
            new_default_payment_method_id: The ID of the new default payment method.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            UserPaymentMethod: The updated default payment method.

        Raises:
            ForbiddenException: If the user does not have permission to set the default payment method.
        """
        unset_default_payment_method_query = (
            update(cls.model)
            .where(cls.model.id == default_payment_method.id)
            .values(is_default=False)
        )

        set_default_payment_method_query = (
            update(cls.model)
            .where(cls.model.id == new_default_payment_method_id)
            .values(is_default=True)
            .returning(cls.model)
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
        """
        Finds a payment method by its ID.

        Args:
            user: The user making the request.
            payment_method_id: The ID of the payment method to find.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            UserPaymentMethod: The found payment method.

        Raises:
            PaymentMethodNotFoundException: If the payment method with the given ID is not found.
            ForbiddenException: If the user does not have permission to access the payment method.
        """
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
        """
        Finds a payment method by its ID.

        Args:
            payment_method_id: The ID of the payment method to find.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            UserPaymentMethod: The found payment method, or None if not found.
        """
        get_payment_method_query = select(cls.model).where(
            cls.model.id == payment_method_id
        )

        payment_method_result = await session.execute(get_payment_method_query)

        payment_method = payment_method_result.scalar_one_or_none()

        return payment_method

    @classmethod
    @manage_session
    async def change_payment_method(
        cls, payment_method_id, user, payment_method_data, session=None
    ):
        """
        Change the details of a payment method.

        Args:
            payment_method_id: The ID of the payment method to change.
            user: The user making the request.
            payment_method_data: The new data for the payment method.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            UserPaymentMethod: The updated payment method.

        Raises:
            PaymentMethodNotFoundException: If the payment method with the given ID is not found.
            ForbiddenException: If the user does not have permission to change the payment method.
            ExpiredCardException: If the new card's expiry date is before today.
            PaymentMethodAlreadyExists: If a payment method with the same account number already exists for another user.
        """
        # Remove none values
        payment_method_data = payment_method_data.model_dump(
            exclude_unset=True
        )

        # Get current payment method
        current_payment_method = await cls._find_by_id(payment_method_id)

        if not current_payment_method:
            raise_http_exception(PaymentMethodNotFoundException)

        if (
            current_payment_method.user_id != user.id
            and user.id not in superior_roles_id
        ):
            raise_http_exception(ForbiddenException)

        # Chanage values with new parameters
        new_payment_method_data = get_new_payment_method_data(
            current_payment_method, payment_method_data
        )

        # if the card is expired
        if new_payment_method_data["expiry_date"] < date.today() + timedelta(
            days=1
        ):
            raise_http_exception(ExpiredCardException)

        # Check if there already exists a card with this account number
        existing_payment_method = await cls._check_payment_method(
            user, new_payment_method_data["account_number"]
        )

        #
        return await cls._handle_existing_or_new_payment_method(
            existing_payment_method,
            user,
            payment_method_id,
            new_payment_method_data,
        )

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
        """
        Handles existing or new payment_method.
        """
        # Payment method exists
        if existing_payment_method:
            if existing_payment_method.user_id == user.id:
                raise_http_exception(PaymentMethodAlreadyExists)
            raise_http_exception(ForbiddenException)

        # If is does not, we can update
        return await cls._update_payment_method(
            new_payment_method_data, payment_method_id
        )

    @classmethod
    @manage_session
    async def _update_payment_method(
        cls, payment_method_data, payment_method_id, session=None
    ):
        """
        Update the details of a payment method.

        Args:
            payment_method_data: The new data for the payment method.
            payment_method_id: The ID of the payment method to update.
            session (Session, optional): The database session. Defaults to None.

        Returns:
            UserPaymentMethod: The updated payment method.

        Raises: PaymentMethodNotFoundException: If the payment method with
        the given ID is not found.
        """
        update_payment_method_query = (
            update(cls.model)
            .where(cls.model.id == payment_method_id)
            .values(**payment_method_data)
            .returning(cls.model)
        )

        updated_payment_method = await session.execute(
            update_payment_method_query
        )
        await session.commit()

        return updated_payment_method.scalars().one()

    @classmethod
    @manage_session
    async def delete_payment_method(
        cls, user, payment_method_id, session=None
    ):
        """
        Delete a payment method.

        Args:
            user: The user making the request.
            payment_method_id: The ID of the payment method to delete.
            session (Session, optional): The database session. Defaults to None.

        Raises:
            PaymentMethodsNotFoundException: If the payment method with the given ID is not found.
            ForbiddenException: If the user does not have permission to delete the payment method.
        """
        # Get current payment method
        payment_method = await cls._find_by_id(payment_method_id)

        if not payment_method:
            raise_http_exception(PaymentMethodsNotFoundException)

        if payment_method.user_id != user.id:
            raise_http_exception(ForbiddenException)

        # If it is default
        if payment_method.is_default:
            new_default_payment_method = await cls._find_payment_method(user)

            # Make some payment method true if this is going to be deleted
            await cls._switch_default_payment_method(
                payment_method, new_default_payment_method.id
            )
        # Delete the payment method
        await cls._delete_certain_payment_method(payment_method_id)

    @classmethod
    @manage_session
    async def _delete_certain_payment_method(
        cls, payment_method_id, session=None
    ):
        """
        Delete a payment method with the given ID.

        Args:
            payment_method_id: The ID of the payment method to delete.
            session (Session, optional): The database session. Defaults to None.
        """
        delete_payment_method_query = delete(cls.model).where(
            cls.model.id == payment_method_id
        )

        await session.execute(delete_payment_method_query)
        await session.commit()

        return None
