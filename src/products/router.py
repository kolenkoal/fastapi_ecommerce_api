from fastapi import APIRouter, Depends, File, Form, UploadFile

from src.auth.auth import current_user
from src.products.categories.router import router as categories_router
from src.products.dao import ProductDAO
from src.products.schemas import SProduct, SProductCreate
from src.users.models import User


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=SProduct)
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


router.include_router(categories_router)
