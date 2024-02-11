from typing import Optional

from pydantic import BaseModel


class SProductCategory(BaseModel):
    id: int
    name: str
    parent_category_id: Optional[int]

    class ConfigDict:
        response_model_exclude_unset = True


class SProductCategories(BaseModel):
    Categories: list[SProductCategory]

    class ConfigDict:
        response_model_exclude_unset = True


class SProductCategoryWithChildren(SProductCategory):
    children_categories: list[SProductCategory]
