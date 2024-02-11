from fastapi import APIRouter

from src.products.categories.router import router as categories_router


router = APIRouter(prefix="/products", tags=["Products"])

router.include_router(categories_router)
