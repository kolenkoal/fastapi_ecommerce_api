from datetime import date, timedelta
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from src.exceptions import (
    ExpiredCardException,
    InvalidCardException,
    WrongAccountNumberException,
    WrongProviderNameException,
)
from src.patterns import LETTER_MATCH_PATTERN, NUMBER_PATTERN
from src.payments.payment_types.schemas import SPaymentType
from src.users.schemas import UserRead


class SPaymentMethodCreate(BaseModel):
    payment_type_id: UUID
    provider: str = Field(min_length=2, max_length=256)
    account_number: str
    expiry_date: date
    is_default: bool

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, value: str):
        if not LETTER_MATCH_PATTERN.match(value):
            raise WrongProviderNameException

        return value.title()

    @field_validator("account_number")
    @classmethod
    def validate_account_number(cls, value: str):
        if not NUMBER_PATTERN.match(value):
            raise WrongAccountNumberException

        if len(value) < 16:
            raise InvalidCardException

        return value

    @field_validator("expiry_date")
    @classmethod
    def validate_expiry_date(cls, expiry_date: date):
        current_date = date.today()
        tomorrow_date = current_date + timedelta(days=1)

        if expiry_date < tomorrow_date:
            raise ExpiredCardException

        return expiry_date

    class Config:
        json_schema_extra = {
            "example": {
                "payment_type_id": "cc4b156a-105c-4033-b28c-1d205c52610b",
                "provider": "Master Card",
                "account_number": "1111111111111111",
                "expiry_date": date.today() + timedelta(days=1),
                "is_default": "true",
            }
        }


class SPaymentMethod(SPaymentMethodCreate):
    id: UUID
    user_id: UUID


class SPaymentMethodWithPaymentType(BaseModel):
    id: UUID
    provider: str
    account_number: str
    expiry_date: date
    is_default: bool
    payment_type: SPaymentType


class SUserPaymentMethod(UserRead):
    payment_methods: list[SPaymentMethodWithPaymentType]
