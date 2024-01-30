from fastapi import APIRouter, Depends

from src.addresses.dao import AddressDAO
from src.addresses.schemas import SAddressCreate
from src.auth.auth import fastapi_users
from src.examples import example_address
from src.exceptions import AddressNotImplmentedException
from src.users.models import User


current_user = fastapi_users.current_user()

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("")
async def add_address(
    address_data: SAddressCreate = example_address,
    user: User = Depends(current_user),
):
    address = await AddressDAO.add(user, **address_data.model_dump())

    if not address:
        raise AddressNotImplmentedException

    return address
