from uuid import UUID

from fastapi import APIRouter

from src.exceptions import raise_http_exception
from src.payments.types.dao import PaymentTypeDAO
from src.payments.types.exceptions import (
    PaymentTypeNotFoundException,
    PaymentTypesNotFoundException,
)
from src.payments.types.responses import (
    PAYMENT_TYPES_NOT_FOUND_RESPONSE,
    PAYMENT_TYPES_SUCCESS_NOT_FOUND_RESPONSE,
)
from src.payments.types.schemas import SPaymentType


router = APIRouter(prefix="/types")


@router.get(
    "",
    name="Get all payment types.",
    responses=PAYMENT_TYPES_SUCCESS_NOT_FOUND_RESPONSE,
)
async def get_all_payment_types():
    payment_types = await PaymentTypeDAO.find_all()

    if not payment_types:
        raise_http_exception(PaymentTypesNotFoundException)

    return payment_types


@router.get(
    "/{payment_type_id}",
    name="Get certain payment type.",
    response_model=SPaymentType,
    responses=PAYMENT_TYPES_NOT_FOUND_RESPONSE,
)
async def get_payment_type_by_id(payment_type_id: UUID):
    payment_type = await PaymentTypeDAO.find_by_id(payment_type_id)

    if not payment_type:
        raise_http_exception(PaymentTypeNotFoundException)

    return payment_type
