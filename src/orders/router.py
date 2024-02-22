from fastapi import APIRouter

from src.orders.statuses.router import router as router_statuses


router = APIRouter(prefix="/orders", tags=["Orders"])

router.include_router(router_statuses)
