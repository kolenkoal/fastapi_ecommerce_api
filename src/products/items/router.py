from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile

from src.auth.auth import current_user
from src.products.items.dao import ProductItemDAO
from src.products.items.schemas import SProductItem, SProductItemCreate
from src.responses import (
    UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
from src.users.models import User


router = APIRouter(prefix="/items")


@router.post(
    "",
    response_model=SProductItem,
    name="Add product item.",
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
async def create_product(
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
