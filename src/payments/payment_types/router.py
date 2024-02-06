from uuid import UUID

from fastapi import APIRouter

from src.exceptions import (
    PaymentTypeNotFoundException,
    PaymentTypesNotFoundException,
    raise_http_exception,
)
from src.payments.payment_types.dao import PaymentTypeDAO
from src.payments.payment_types.schemas import SPaymentType
from src.responses import (
    PAYMENT_TYPES_NOT_FOUND_RESPONSE,
    PAYMENT_TYPES_SUCCESS_NOT_FOUND_RESPONSE,
)


router = APIRouter(prefix="/payment_types", tags=["Payment Types"])


@router.get(
    "",
    name="Get all payment types.",
    responses=PAYMENT_TYPES_SUCCESS_NOT_FOUND_RESPONSE,
)
async def get_payment_types():
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
async def get_payment_type(payment_type_id: UUID):
    payment_type = await PaymentTypeDAO.find_by_id(payment_type_id)

    if not payment_type:
        raise_http_exception(PaymentTypeNotFoundException)

    return payment_type
