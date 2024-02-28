from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi_users import exceptions
from fastapi_users.authentication import Authenticator, JWTStrategy
from fastapi_users.router.common import ErrorCode
from pydantic import EmailStr

from src.auth.auth import auth_backend, get_jwt_strategy
from src.auth.exceptions import (
    LoginBadCredentialsExceptions,
    UserAlreadyExistsException,
)
from src.auth.forms import LoginForm
from src.auth.manager import UserManager, get_user_manager
from src.auth.responses import (
    LOGIN_RESPONSE,
    LOGOUT_RESPONSE,
    REGISTER_RESPONSE,
    RESET_PASSWORD_RESPONSE,
)
from src.shopping_carts.router import create_shopping_cart
from src.shopping_carts.schemas import SShoppingCartCreate
from src.users.profiles.router import create_user_profile
from src.users.schemas import UserCreate, UserRead


router = APIRouter(prefix="/auth", tags=["Auth"])

authenticator = Authenticator([auth_backend], get_user_manager)

get_current_user_token = authenticator.current_user_token(active=True)


@router.post(
    "/login",
    name="Login A registered User.",
    responses=LOGIN_RESPONSE,
)
async def login(
    request: Request,
    credentials: LoginForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager),
    strategy: JWTStrategy = Depends(get_jwt_strategy),
):
    user = await user_manager.authenticate(credentials)

    if user is None or not user.is_active:
        raise LoginBadCredentialsExceptions

    response = await auth_backend.login(strategy, user)
    await user_manager.on_after_login(user, request, response)
    return response


@router.post(
    "/logout", name="Logout logged in User", responses=LOGOUT_RESPONSE
)
async def logout(
    user_token=Depends(get_current_user_token),
    strategy: JWTStrategy = Depends(get_jwt_strategy),
):
    user, token = user_token
    return await auth_backend.logout(strategy, user, token)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    name="Register a new User.",
    responses=REGISTER_RESPONSE,
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
        raise UserAlreadyExistsException
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

    await create_user_profile(created_user)

    return created_user


@router.post(
    "/forgot-password",
    status_code=status.HTTP_202_ACCEPTED,
    name="Ask for reset of forgotten password",
)
async def forgot_password(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        user = await user_manager.get_by_email(email)
    except exceptions.UserNotExists:
        return None

    try:
        await user_manager.forgot_password(user, request)
    except exceptions.UserInactive:
        pass

    return None


@router.post(
    "/reset-password",
    name="Reset forgotten password",
    responses=RESET_PASSWORD_RESPONSE,
)
async def reset_password(
    request: Request,
    token: str = Body(...),
    password: str = Body(...),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        await user_manager.reset_password(token, password, request)
    except (
        exceptions.InvalidResetPasswordToken,
        exceptions.UserNotExists,
        exceptions.UserInactive,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
