from typing import Optional

from pydantic import BaseModel, field_validator

from src.patterns import LETTER_MATCH_PATTERN
from src.payments.types.exceptions import WrongPaymentTypeNameException


class SOrderStatusCreate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_name(cls, name: str):
        if not LETTER_MATCH_PATTERN.match(name):
            raise WrongPaymentTypeNameException

        return name.title()


class SOrderStatus(BaseModel):
    id: int
    status: str


class SOrderStatusCreateOptional(BaseModel):
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_name(cls, name: str):
        if not LETTER_MATCH_PATTERN.match(name):
            raise WrongPaymentTypeNameException

        return name.title()


class SOrderStatuses(BaseModel):
    order_statuses: list[SOrderStatus]
