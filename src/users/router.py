from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users import exceptions
from fastapi_users.router import ErrorCode

from src.auth.auth import current_user
from src.auth.manager import UserManager, get_user_manager
from src.permissions import has_permission
from src.users.dao import UserDAO
from src.users.exceptions import NotFoundException, UserAlreadyExistsException
from src.users.models import User
from src.users.profiles.router import router as router_profiles
from src.users.responses import (
    PATCH_ME_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)
from src.users.reviews.router import router as router_reviews
from src.users.schemas import UserRead, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

router.include_router(router_reviews)
router.include_router(router_profiles)


# router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))


@router.get(
    "/me",
    response_model=UserRead,
    name="Get Current User",
    responses=UNAUTHORIZED_RESPONSE,
)
async def me(user: User = Depends(current_user)):
    return user


@router.patch(
    "/me",
    response_model=UserRead,
    name="Change Current User",
    responses=PATCH_ME_RESPONSE,
)
async def update_me(
    request: Request,
    user_update_data: UserUpdate,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        user = await user_manager.update(
            user_update_data, user, safe=True, request=request
        )
        return user
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except exceptions.UserAlreadyExists:
        raise UserAlreadyExistsException


@router.get(
    "/{id}",
    response_model=UserRead,
    name="Get User By Id",
    responses=UNAUTHORIZED_FORBIDDEN_NOT_FOUND_RESPONSE,
)
async def get_user(user_id: UUID, user: User = Depends(current_user)):
    found_user = await UserDAO.find_one_or_none(id=user_id)

    if not found_user:
        raise NotFoundException

    if await has_permission(user):
        return found_user

    if user.id == found_user.id:
        return user

    raise NotFoundException


@router.patch(
    "/{id}",
    response_model=UserRead,
    name="Change User by Id",
    responses=UNAUTHORIZED_FORBIDDEN_NOT_FOUND_RESPONSE,
)
async def update_user(
    id: UUID,
    user_update_data: UserUpdate,  # type: ignore
    request: Request,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        found_user = await UserDAO.find_one_or_none(id=id)

        if not found_user:
            raise NotFoundException

        if not await has_permission(user) and user.id != found_user.id:
            raise NotFoundException

        if await has_permission(user):
            found_user = await user_manager.update(
                user_update_data, found_user, safe=True, request=request
            )

            return found_user
        else:
            user = await user_manager.update(
                user_update_data, user, safe=True, request=request
            )

            return user
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except exceptions.UserAlreadyExists:
        raise UserAlreadyExistsException


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete User By Id.",
    responses=UNAUTHORIZED_FORBIDDEN_NOT_FOUND_RESPONSE,
)
async def delete_user(
    id: UUID,
    request: Request,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    found_user = await UserDAO.find_one_or_none(id=id)

    if not found_user:
        raise NotFoundException

    if not await has_permission(user):
        raise NotFoundException

    await user_manager.delete(found_user, request=request)
    return None
