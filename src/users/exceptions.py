from fastapi import HTTPException, status
from fastapi_users.router import ErrorCode

from src.exceptions import EcommerceException


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
)

NotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="The user does not exist.",
)


class WrongNameOrSurnameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid First Name or Last Name."
