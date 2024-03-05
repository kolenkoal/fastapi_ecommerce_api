from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from starlette import status

from src.auth.auth import current_user
from src.exceptions import (
    ProductConfigurationsNotFoundException,
    UserReviewsNotFoundException,
    raise_http_exception,
)
from src.products.items.dao import ProductItemDAO
from src.products.items.exceptions import (
    ProductItemNotFoundException,
    ProductItemsNotFoundException,
)
from src.products.items.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_NOT_FOUND_RESPONSE,
    PRODUCT_ITEM_NOT_FOUND,
    PRODUCT_ITEMS_NOT_FOUND,
)
from src.products.items.schemas import (
    SProductItem,
    SProductItemCreate,
    SProductItemCreateOptional,
    SProductItems,
    SProductItemWithProduct,
    SProductItemWithVariations,
)
from src.products.responses import (
    UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
from src.users.models import User
from src.users.reviews.schemas import SUserReviews


router = APIRouter(prefix="/items")


@router.post(
    "",
    response_model=SProductItem,
    name="Add product item.",
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
async def create_product_item(
    file: UploadFile = File(...),
    price: Decimal = Form(...),
    quantity_in_stock: int = Form(...),
    product_id: UUID = Form(...),
    user: User = Depends(current_user),
):
    product_item_data = SProductItemCreate(
        price=price, quantity_in_stock=quantity_in_stock, product_id=product_id
    )

    product_item = await ProductItemDAO.add(user, product_item_data, file)

    return product_item


@router.get(
    "",
    name="Get all product items.",
    response_model=SProductItems,
    responses=PRODUCT_ITEMS_NOT_FOUND,
)
async def get_all_product_items():
    product_items = await ProductItemDAO.find_all()

    if not product_items:
        raise_http_exception(ProductItemsNotFoundException)

    return {"product_items": product_items}


@router.get(
    "/{product_item_id}",
    name="Get certain product item.",
    response_model=SProductItemWithProduct,
    responses=PRODUCT_ITEM_NOT_FOUND,
)
async def get_product_item_by_id(product_item_id: UUID):
    product_item = await ProductItemDAO.find_by_id(product_item_id)

    if not product_item:
        raise_http_exception(ProductItemNotFoundException)

    return product_item


@router.get(
    "/{product_item_id}/configurations",
    name="Get all product item configurations.",
    response_model=SProductItemWithVariations,
    responses=PRODUCT_ITEM_NOT_FOUND,
)
async def get_product_item_configurations(product_item_id: UUID):
    product_item = await ProductItemDAO.get_product_item_configurations(
        product_item_id
    )

    if not product_item:
        raise_http_exception(ProductItemNotFoundException)

    if not product_item.__dict__["variations"]:
        raise_http_exception(ProductConfigurationsNotFoundException)

    return product_item


@router.get(
    "/{product_item_id}/reviews",
    name="Get all product item reviews.",
    response_model=SUserReviews,
    responses=PRODUCT_ITEM_NOT_FOUND,
)
async def get_product_item_reviews(product_item_id: UUID):
    user_reviews = await ProductItemDAO.get_product_item_reviews(
        product_item_id
    )

    if not user_reviews:
        raise_http_exception(UserReviewsNotFoundException)

    return {"user_reviews": user_reviews}


@router.patch(
    "/{product_item_id}",
    response_model=SProductItem,
    response_model_exclude_none=True,
    name="Change certain product item.",
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
async def change_product_item_by_id(
    product_item_id: UUID,
    data: SProductItemCreateOptional,
    user: User = Depends(current_user),
):
    product_item = await ProductItemDAO.change(product_item_id, user, data)

    if not product_item:
        raise ProductItemNotFoundException

    return product_item


@router.delete(
    "/{product_item_id}",
    name="Delete certain product item.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_NOT_FOUND_RESPONSE,
)
async def delete_product_item_by_id(
    product_item_id: UUID,
    user: User = Depends(current_user),
):
    product_item = await ProductItemDAO.delete(user, product_item_id)

    if not product_item:
        return {"detail": "The product item was deleted."}
