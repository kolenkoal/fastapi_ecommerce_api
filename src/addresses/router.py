from fastapi import APIRouter, Depends

from src.addresses.dao import AddressDAO
from src.addresses.schemas import SAddressCreate
from src.auth.auth import fastapi_users
from src.exceptions import AddressNotImplmentedException
from src.users.models import User


current_user = fastapi_users.current_user()

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("")
async def add_address(
    address_data: SAddressCreate, user: User = Depends(current_user)  # noqa
):
    address = await AddressDAO.add(**address_data.model_dump())

    if not address:
        raise AddressNotImplmentedException

    return address
