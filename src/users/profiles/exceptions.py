from fastapi import status

from src.exceptions import EcommerceException


class UserProfileNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User profile not found."


class UserAlreadyHasProfileException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "User already has a profile."


class UserProfileNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add user profile."
