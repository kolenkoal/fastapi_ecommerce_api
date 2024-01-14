from fastapi import APIRouter

from src.auth.auth import fastapi_users
from src.users.schemas import UserRead, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))
