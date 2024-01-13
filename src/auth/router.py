from fastapi import APIRouter

from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserCreate, UserRead


router = APIRouter(prefix="/auth/jwt", tags=["auth"])

router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserRead))
