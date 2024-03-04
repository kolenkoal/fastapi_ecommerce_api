import uuid

from pydantic import BaseModel, field_validator

from src.patterns import LETTER_MATCH_PATTERN
from src.payments.types.exceptions import WrongPaymentTypeNameException


class SPaymentTypeCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str):
        if not LETTER_MATCH_PATTERN.match(name):
            raise WrongPaymentTypeNameException

        return name.title()


class SPaymentType(SPaymentTypeCreate):
    id: uuid.UUID
