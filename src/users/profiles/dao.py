from src.dao import BaseDAO
from src.exceptions import raise_http_exception
from src.images.router import add_profile_image
from src.users.profiles.exceptions import UserAlreadyHasProfileException
from src.users.profiles.models import UserProfile
from src.utils.data_manipulation import get_new_data
from src.utils.session import manage_session


class UserProfileDAO(BaseDAO):
    model = UserProfile

    @classmethod
    @manage_session
    async def add(cls, user, session=None):
        await cls._check_profile_exists(user)

        return await cls._create(user_id=user.id)

    @classmethod
    @manage_session
    async def _check_profile_exists(cls, user, session=None):
        user_profile = await cls.find_one_or_none(user_id=user.id)

        if user_profile:
            raise_http_exception(UserAlreadyHasProfileException)

    @classmethod
    @manage_session
    async def change(cls, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        current_user_profile = await cls.find_one_or_none(user_id=user.id)

        if not current_user_profile:
            return None

        if not data:
            return current_user_profile

        new_shopping_cart_data = get_new_data(current_user_profile, data)

        return await cls.update_data(
            current_user_profile.id, new_shopping_cart_data
        )

    @classmethod
    @manage_session
    async def change_image(cls, user, file, session=None):
        profile_image_name = f"{user.id}.webp"

        # Upload the given file to images
        uploaded_image_name = await add_profile_image(profile_image_name, file)

        current_profile = await cls.find_one_or_none(user_id=user.id)

        return await cls.update_data(
            current_profile.id, {"profile_image": uploaded_image_name}
        )
