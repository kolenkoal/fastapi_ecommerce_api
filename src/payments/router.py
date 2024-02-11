from fastapi import APIRouter

from src.payments.payment_methods.router import (
    router as payment_methods_router,
)
from src.payments.payment_types.router import router as payment_types_router


router = APIRouter(prefix="/payments", tags=["Payments"])

router.include_router(payment_types_router)
router.include_router(payment_methods_router)
