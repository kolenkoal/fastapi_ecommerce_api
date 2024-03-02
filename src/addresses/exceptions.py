from fastapi import status

from src.exceptions import EcommerceException


class AddressesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Addresses not found."


class AddressNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Address not found."


class DefaultAddressNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "You do not have default address."


class UserHasNoAddressesException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "You do not have any addresses."


class NoSuchAddressException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such address."


class WrongCityOrRegionException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid City, Region or Address Line."


class UserAlreadyHasThisAddress(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "You already have this address added."


class AddressNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add address."
