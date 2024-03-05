from typing import Optional, Type, Union
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.patterns import LETTER_MATCH_PATTERN, REMOVE_WHITESPACES
from src.products.categories.schemas import SProductCategory
from src.products.schemas import SProduct
from src.variations.exceptions import WrongVariationNameException
from src.variations.options.schemas import SVariationOption


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


class SVariationCreateOptional(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None

    @field_validator("name")
    @classmethod
    def validate_category_name(
        cls, value: str
    ) -> Union[str, Type[WrongVariationNameException]]:
        if not LETTER_MATCH_PATTERN.match(value):
            raise WrongVariationNameException
        value = REMOVE_WHITESPACES(value)
        return value.title()


class SVariationWithCategoryAndOptions(BaseModel):
    id: UUID
    name: str
    category: SProductCategory
    options: list[SVariationOption]


class SProductCategoryWithVariations(SProductCategory):
    variations: list[SVariation]


class SProductCategoryWithProducts(SProductCategory):
    products: list[SProduct]


class SVariations(BaseModel):
    variations: list[SVariation]
