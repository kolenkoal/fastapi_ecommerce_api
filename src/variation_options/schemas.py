from typing import Optional, Type, Union
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.exceptions import WrongVariationOptionNameException
from src.patterns import ALPHA_NUMBERS_PATTERN, REMOVE_WHITESPACES


class SVariationOptionCreate(BaseModel):
    value: str
    variation_id: UUID

    @field_validator("value")
    @classmethod
    def validate_option_value(
        cls, value: str
    ) -> Union[str, Type[WrongVariationOptionNameException]]:
        if not ALPHA_NUMBERS_PATTERN.match(value):
            raise WrongVariationOptionNameException
        value = REMOVE_WHITESPACES(value)
        return value


class SVariationOptionCreateOptional(BaseModel):
    value: Optional[str] = None
    variation_id: Optional[UUID] = None

    @field_validator("value")
    @classmethod
    def validate_option_value(
        cls, value: str
    ) -> Union[str, Type[WrongVariationOptionNameException]]:
        if not ALPHA_NUMBERS_PATTERN.match(value):
            raise WrongVariationOptionNameException
        value = REMOVE_WHITESPACES(value)
        return value


class SVariationOption(BaseModel):
    id: UUID
    value: str
    variation_id: UUID


class SVariationOptions(BaseModel):
    variation_options: list[SVariationOption]
