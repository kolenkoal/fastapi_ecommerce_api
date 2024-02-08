from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.exceptions import (
    PaymentMethodNotFoundException,
    PaymentMethodsNotFoundException,
    raise_http_exception,
)
from src.payments.user_payment_methods.dao import UserPaymentMethodDAO
from src.payments.user_payment_methods.schemas import (
    SPaymentMethod,
    SPaymentMethodCreate,
    SPaymentMethodCreateOptional,
    SUserPaymentMethod,
    SUsersPaymentMethods,
)
from src.responses import (
    UNAUTHORIZED_FORBIDDEN_PAYMENT_METHOD_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_PAYMENT_METHODS_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)
from src.users.models import User


router = APIRouter(prefix="/payment_methods", tags=["Payment Methods"])


@router.post(
    "",
    name="Create a payment method.",
    response_model=SPaymentMethod,
    responses=UNAUTHORIZED_RESPONSE,
)
async def create_payment_method(
    payment_method_data: SPaymentMethodCreate,
    user: User = Depends(current_user),
):
    payment_method = await UserPaymentMethodDAO.add_payment_method(
        user, **payment_method_data.model_dump()
    )

    if not payment_method:
        raise_http_exception(PaymentMethodNotFoundException)

    return payment_method


@router.get(
    "",
    name="Get all user payment methods.",
    response_model=Union[SUserPaymentMethod, SUsersPaymentMethods],
    responses=UNAUTHORIZED_PAYMENT_METHODS_NOT_FOUND_RESPONSE,
)
async def get_payment_methods(user: User = Depends(current_user)):
    payment_methods = await UserPaymentMethodDAO.find_all(user)

    if not payment_methods:
        raise_http_exception(PaymentMethodsNotFoundException)

    return payment_methods


@router.get(
    "/{payment_method_id}",
    response_model=SPaymentMethod,
    name="Get certain payment method.",
    responses=UNAUTHORIZED_FORBIDDEN_PAYMENT_METHOD_NOT_FOUND_RESPONSE,
)
async def get_payment_method(
    payment_method_id: UUID, user: User = Depends(current_user)
):
    payment_method = await UserPaymentMethodDAO.find_payment_method(
        user, payment_method_id
    )

    if not payment_method:
        raise PaymentMethodNotFoundException

    return payment_method


@router.patch(
    "/{payment_method_id}",
    response_model=SPaymentMethod,
    response_model_exclude_none=True,
    name="Change certain payment method.",
    responses=UNAUTHORIZED_FORBIDDEN_PAYMENT_METHOD_NOT_FOUND_RESPONSE,
)
async def change_user_payment_method(
    payment_method_id: UUID,
    payment_method_data: SPaymentMethodCreateOptional,
    user: User = Depends(current_user),
):
    payment_method = await UserPaymentMethodDAO.change_payment_method(
        payment_method_id, user, payment_method_data
    )

    if not payment_method:
        raise PaymentMethodNotFoundException

    return payment_method
