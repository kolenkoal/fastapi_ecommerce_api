from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users import exceptions
from fastapi_users.router.common import ErrorCode, ErrorModel

from src.auth.auth import auth_backend, fastapi_users
from src.auth.manager import UserManager, get_user_manager
from src.shopping_carts.router import create_shopping_cart
from src.shopping_carts.schemas import SShoppingCartCreate
from src.users.schemas import UserCreate, UserRead


router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(fastapi_users.get_auth_router(auth_backend))


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    name="register:register",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.REGISTER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                    "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def register(
    request: Request,
    user_create: UserCreate,  # type: ignore
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        created_user = await user_manager.create(
            user_create, safe=True, request=request
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    shopping_cart_data = SShoppingCartCreate(user_id=created_user.id)
    await create_shopping_cart(shopping_cart_data, created_user)
    return created_user


router.include_router(fastapi_users.get_reset_password_router())
