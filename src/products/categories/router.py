from fastapi import APIRouter, status

from src.exceptions import (
    CategoriesNotFoundException,
    CategoryNotFoundException,
    raise_http_exception,
)
from src.products.categories.dao import ProductCategoryDAO
from src.products.categories.schemas import (
    SProductCategories,
    SProductCategoryWithChildren,
)


router = APIRouter(prefix="/categories")


@router.get(
    "",
    name="Get all categories.",
    response_model=SProductCategories,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Man",
                        },
                        {"id": 4, "name": "Tops", "parent_category_id": 1},
                    ]
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "examples": {
                        "Categories not found.": {
                            "summary": "Categories not found.",
                            "value": {"detail": "Categories not found."},
                        },
                    }
                }
            }
        },
    },
)
async def get_categories():
    categories = await ProductCategoryDAO.find_all()

    if not categories:
        raise CategoriesNotFoundException

    return {"Categories": categories}


@router.get(
    "/{category_id}",
    name="Get certain category.",
    response_model=SProductCategoryWithChildren,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "examples": {
                        "Category not found.": {
                            "summary": "Category not found.",
                            "value": {"detail": "Category not found."},
                        },
                    }
                }
            }
        }
    },
)
async def get_category(category_id: int):
    category = await ProductCategoryDAO.find_by_id(category_id)

    if not category:
        raise_http_exception(CategoryNotFoundException)

    return category
