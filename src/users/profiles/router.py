from fastapi import APIRouter, Depends, File, UploadFile

from src.auth.auth import current_user
from src.exceptions import raise_http_exception
from src.responses import UNAUTHORIZED_RESPONSE
from src.users.models import User
from src.users.profiles.dao import UserProfileDAO
from src.users.profiles.exceptions import (
    UserProfileNotFoundException,
    UserProfileNotImplementedException,
)
from src.users.profiles.schemas import SUserProfile, SUserProfileCreateOptional


router = APIRouter(prefix="/profile")


@router.post(
    "",
    name="Create user profile",
    response_model=SUserProfile,
    responses=UNAUTHORIZED_RESPONSE,
)
async def create_user_profile(
    user: User = Depends(current_user),
):
    user_profile = await UserProfileDAO.add(user)

    if not user_profile:
        raise_http_exception(UserProfileNotImplementedException)

    return user_profile


@router.get(
    "",
    name="Get user profile.",
    response_model=SUserProfile,
    responses=UNAUTHORIZED_RESPONSE,
)
async def get_user_profile(user: User = Depends(current_user)):
    user_profile = await UserProfileDAO.find_one_or_none(user_id=user.id)

    if not user_profile:
        raise_http_exception(UserProfileNotFoundException)

    return user_profile


@router.patch(
    "/bio",
    response_model=SUserProfile,
    name="Change user profile bio.",
    responses=UNAUTHORIZED_RESPONSE,
)
async def change_user_profile(
    data: SUserProfileCreateOptional,
    user: User = Depends(current_user),
):
    user_profile = await UserProfileDAO.change(user, data)

    if not user_profile:
        raise_http_exception(UserProfileNotFoundException)

    return user_profile


@router.patch(
    "/image",
    response_model=SUserProfile,
    name="Change user profile image.",
    responses=UNAUTHORIZED_RESPONSE,
)
async def update_user_profile_image(
    file: UploadFile = File(...), user: User = Depends(current_user)
):
    user_profile = await UserProfileDAO.change_image(user, file)

    return user_profile
