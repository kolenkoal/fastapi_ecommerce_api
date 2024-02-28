from fastapi import HTTPException, status
from fastapi_users.router import ErrorCode


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
)

LoginBadCredentialsExceptions = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
)
