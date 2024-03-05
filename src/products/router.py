from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from starlette import status

from src.auth.auth import current_user
from src.exceptions import ProductItemsNotFoundException, raise_http_exception
from src.products.categories.responses import (
    UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
from src.products.categories.router import router as categories_router
from src.products.configurations.router import router as configurations_router
from src.products.dao import ProductDAO
from src.products.exceptions import (
    ProductNotFoundException,
    ProductsNotFoundException,
)
from src.products.items.router import router as items_router
from src.products.items.schemas import SProductWithItems
from src.products.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_RESPONSE,
    PRODUCT_NOT_FOUND,
    PRODUCTS_NOT_FOUND,
    UNAUTHORIZED_FORBIDDEN_CATEGORY_OR_PRODUCT_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
from src.products.schemas import (
    SProduct,
    SProductCreate,
    SProductCreateOptional,
    SProducts,
    SProductWithCategory,
)
from src.users.models import User


router = APIRouter(prefix="/products", tags=["Products"])

router.include_router(categories_router)
router.include_router(items_router)
router.include_router(configurations_router)


@router.post(
    "",
    response_model=SProduct,
    name="Add product to the category.",
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
async def create_product(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    user: User = Depends(current_user),
):
    product_data = SProductCreate(
        name=name, description=description, category_id=category_id
    )

    product = await ProductDAO.add(user, product_data, file)

    return product


@router.get(
    "",
    name="Get all products.",
    response_model=SProducts,
    responses=PRODUCTS_NOT_FOUND,
)
async def get_all_products():
    products = await ProductDAO.find_all()

    if not products:
        raise_http_exception(ProductsNotFoundException)

    return {"products": products}


@router.get(
    "/{product_id}",
    name="Get certain product.",
    response_model=SProductWithCategory,
    responses=PRODUCT_NOT_FOUND,
)
async def get_product_by_id(product_id: UUID):
    product = await ProductDAO.find_by_id(product_id)

    if not product:
        raise_http_exception(ProductNotFoundException)

    return product


@router.get(
    "/{product_id}/product_items",
    name="Get all product items of product.",
    response_model=SProductWithItems,
    responses=PRODUCT_NOT_FOUND,
)
async def get_product_product_items(product_id: UUID):
    product = await ProductDAO.get_product_product_items(product_id)

    if not product:
        raise_http_exception(ProductNotFoundException)

    if not product.__dict__["product_items"]:
        raise_http_exception(ProductItemsNotFoundException)

    return product


@router.patch(
    "/{product_id}",
    response_model=SProduct,
    response_model_exclude_none=True,
    name="Change certain product.",
    responses=UNAUTHORIZED_FORBIDDEN_CATEGORY_OR_PRODUCT_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
async def change_product_by_id(
    product_id: UUID,
    data: SProductCreateOptional,
    user: User = Depends(current_user),
):
    product = await ProductDAO.change(product_id, user, data)

    if not product:
        raise ProductNotFoundException

    return product


@router.delete(
    "/{product_id}",
    name="Delete certain product.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_RESPONSE,
)
async def delete_product_by_id(
    product_id: UUID,
    user: User = Depends(current_user),
):
    product = await ProductDAO.delete(user, product_id)

    if not product:
        return {"detail": "The product was deleted."}
