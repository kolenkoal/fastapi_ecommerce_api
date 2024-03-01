from fastapi import status
from fastapi_users.router.common import ErrorCode, ErrorModel


UNAUTHORIZED_RESPONSE = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    }
}
FORBIDDEN_RESPONSE = {
    status.HTTP_403_FORBIDDEN: {
        "description": "Not a superuser.",
    },
}

NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "description": "The user does not exist.",
    },
}

PATCH_ME_RESPONSE = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                        "summary": "A user with this email already exists.",
                        "value": {
                            "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                        },
                    },
                    ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                "reason": "Password should be"
                                "at least 3 characters",
                            }
                        },
                    },
                }
            }
        },
    },
    **UNAUTHORIZED_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **NOT_FOUND_RESPONSE,
}
