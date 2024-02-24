from fastapi import APIRouter

from src.auth.auth import fastapi_users
from src.users.reviews.router import router as router_reviews
from src.users.schemas import UserRead, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

router.include_router(router_reviews)
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))
