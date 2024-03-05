from fastapi import status

from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)


PAYMENT_METHODS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Payment methods not found.": {
                        "summary": "Payment methods not found.",
                        "value": {"detail": "Payment methods not found."},
                    },
                }
            }
        }
    },
}

PAYMENT_METHOD_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Payment method not found.": {
                        "summary": "Payment method not found.",
                        "value": {"detail": "Payment method not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_PAYMENT_METHODS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **PAYMENT_METHODS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_PAYMENT_METHOD_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PAYMENT_METHOD_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PAYMENT_METHOD_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PAYMENT_METHOD_NOT_FOUND_RESPONSE,
}
