from typing import Optional, Type, Union

from pydantic import BaseModel, field_validator

from src.exceptions import WrongCategoryNameException
from src.patterns import LETTER_MATCH_PATTERN, REMOVE_WHITESPACES


class SProductCategoryCreate(BaseModel):
    name: str
    parent_category_id: Optional[int] = None

    @field_validator("name")
    @classmethod
    def validate_category_name(
        cls, value: str
    ) -> Union[str, Type[WrongCategoryNameException]]:
        if not LETTER_MATCH_PATTERN.match(value):
            raise WrongCategoryNameException
        value = REMOVE_WHITESPACES(value)
        return value.title()

    class ConfigDict:
        response_model_exclude_unset = True


class SProductCategoryOptional(BaseModel):
    name: Optional[str] = None
    parent_category_id: Optional[int] = None

    @field_validator("name")
    @classmethod
    def validate_category_name(
        cls, value: str
    ) -> Union[str, Type[WrongCategoryNameException]]:
        if not LETTER_MATCH_PATTERN.match(value):
            raise WrongCategoryNameException
        value = REMOVE_WHITESPACES(value)
        return value.title()

    class ConfigDict:
        response_model_exclude_unset = True


class SProductCategory(BaseModel):
    id: int
    name: str
    parent_category_id: Optional[int]


class SProductCategories(BaseModel):
    product_categories: list[SProductCategory]


class SProductCategoryWithChildren(SProductCategory):
    children_categories: list[SProductCategory]
