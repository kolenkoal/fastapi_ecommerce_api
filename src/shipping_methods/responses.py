from fastapi import status

from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)


SHIPPING_METHOD_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shipping method not found.": {
                        "summary": "Shipping method not found.",
                        "value": {"detail": "Shipping method not found."},
                    },
                }
            }
        }
    },
}

SHIPPING_METHODS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shipping methods not found.": {
                        "summary": "Shipping methods not found.",
                        "value": {"detail": "Shipping methods not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_SHIPPING_METHOD_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHIPPING_METHOD_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_SHIPPING_METHOD_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHIPPING_METHOD_NOT_FOUND_RESPONSE,
}
