from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.examples import example_product_category
from src.exceptions import (
    CategoryNotFoundException,
    ProductCategoriesNotFoundException,
    ProductCategoryNotFoundException,
    ProductCategoryNotImplementedException,
    raise_http_exception,
)
from src.products.categories.dao import ProductCategoryDAO
from src.products.categories.schemas import (
    SProductCategories,
    SProductCategory,
    SProductCategoryCreate,
    SProductCategoryOptional,
    SProductCategoryWithChildren,
)
from src.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE,
    PRODUCT_CATEGORY_NOT_FOUND,
    UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_PARENT_CATEGORY_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
from src.users.models import User


router = APIRouter(prefix="/categories")


@router.post(
    "",
    response_model=SProductCategory,
    name="Add product category.",
    responses=UNAUTHORIZED_PARENT_CATEGORY_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
async def add_product_category(
    product_category_data: SProductCategoryCreate = example_product_category,
    user: User = Depends(current_user),
):
    product_category = await ProductCategoryDAO.add(
        user, product_category_data
    )

    if not product_category:
        raise ProductCategoryNotImplementedException

    return product_category


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
        raise ProductCategoriesNotFoundException

    return {"product_categories": categories}


@router.get(
    "/{product_category_id}",
    name="Get certain product category.",
    response_model=SProductCategoryWithChildren,
    responses=PRODUCT_CATEGORY_NOT_FOUND,
)
async def get_category(product_category_id: int):
    category = await ProductCategoryDAO.find_by_id(product_category_id)

    if not category:
        raise_http_exception(CategoryNotFoundException)

    return category


@router.patch(
    "/{product_category_id}",
    response_model=SProductCategory,
    response_model_exclude_none=True,
    name="Change certain product category.",
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE,
)
async def change_user_address(
    product_category_id: int,
    data: SProductCategoryOptional,
    user: User = Depends(current_user),
):
    product_category = await ProductCategoryDAO.change(
        product_category_id, user, data
    )

    if not product_category:
        raise ProductCategoryNotFoundException

    return product_category


@router.delete(
    "/{product_category_id}",
    name="Delete certain product category.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE,
)
async def delete_user_address(
    product_category_id: int,
    user: User = Depends(current_user),
):
    product_category = await ProductCategoryDAO.delete(
        user, product_category_id
    )

    if not product_category:
        return {"detail": "The product category was deleted."}
