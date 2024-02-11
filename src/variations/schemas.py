from typing import Type, Union
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.exceptions import WrongVariationNameException
from src.patterns import LETTER_MATCH_PATTERN, REMOVE_WHITESPACES


class SVariationCreate(BaseModel):
    name: str
    category_id: int

    @field_validator("name")
    @classmethod
    def validate_category_name(
        cls, value: str
    ) -> Union[str, Type[WrongVariationNameException]]:
        if not LETTER_MATCH_PATTERN.match(value):
            raise WrongVariationNameException
        value = REMOVE_WHITESPACES(value)
        return value.title()


class SVariation(BaseModel):
    id: UUID
    name: str
    category_id: int
