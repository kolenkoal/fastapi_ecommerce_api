from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.addresses.dao import AddressDAO
from src.addresses.schemas import (
    SAddress,
    SAddressCountry,
    SAddressCreate,
    SAddressOptional,
    SAllUserAddresses,
    SAllUsersAddresses,
)
from src.auth.auth import current_user
from src.examples import example_address
from src.exceptions import (
    AddressNotImplementedException,
    NoSuchAddressException,
    UserHasNoAddressesException,
)
from src.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_ADDRESS_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_COUNTRY_NOT_FOUND_UNPROCESSABLE_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
from src.users.models import User


router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post(
    "",
    response_model=SAddress,
    name="Add address.",
    responses=UNAUTHORIZED_COUNTRY_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
async def add_address(
    address_data: SAddressCreate = example_address,
    user: User = Depends(current_user),
):
    address = await AddressDAO.add(user, **address_data.model_dump())

    if not address:
        raise AddressNotImplementedException

    return address


@router.post(
    "/{address_id}/set_default",
    name="Set an address to default.",
    responses=UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
async def set_address_to_default(
    address_id: UUID, user: User = Depends(current_user)
):
    address = await AddressDAO.set_to_default(address_id, user)

    if not address:
        raise NoSuchAddressException

    return address


@router.get(
    "",
    response_model=Union[SAllUsersAddresses, SAllUserAddresses],
    name="Get all User addresses.",
    responses=UNAUTHORIZED_ADDRESS_NOT_FOUND_RESPONSE,
)
async def get_user_addresses(user: User = Depends(current_user)):
    addresses = await AddressDAO.find_all(user)

    if not addresses:
        raise UserHasNoAddressesException

    return addresses


@router.get(
    "/{address_id}",
    response_model=SAddressCountry,
    name="Get certain address.",
    responses=UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
async def get_address(address_id: UUID, user: User = Depends(current_user)):
    address = await AddressDAO.find_by_id(user, address_id)

    if not address:
        raise NoSuchAddressException

    return address


@router.patch(
    "/{address_id}",
    response_model=SAddressOptional,
    response_model_exclude_none=True,
    name="Change certain address.",
    responses=UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
async def change_user_address(
    address_id: UUID,
    address_data: SAddressOptional,
    user: User = Depends(current_user),
):
    address = await AddressDAO.change_address(address_id, user, address_data)

    if not address:
        raise NoSuchAddressException

    return address


@router.delete(
    "/{address_id}",
    name="Delete certain address.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
async def delete_user_address(
    address_id: UUID,
    user: User = Depends(current_user),
):
    address = await AddressDAO.delete_address(user, address_id)

    if not address:
        return {"detail": "The address was deleted."}
