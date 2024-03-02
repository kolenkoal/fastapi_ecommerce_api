from fastapi import status

from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)


ADDRESS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Addresses not found.": {
                        "summary": "Addresses not found.",
                        "value": {"detail": "Addresses not found."},
                    },
                }
            }
        }
    }
}

UNAUTHORIZED_ADDRESS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
}
