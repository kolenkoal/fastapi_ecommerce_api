from fastapi import status

from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)


ORDER_STATUS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Order status not found.": {
                        "summary": "Order status not found.",
                        "value": {"detail": "Order status not found."},
                    },
                }
            }
        }
    },
}

ORDER_STATUSES_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Order statuses not found.": {
                        "summary": "Order statuses not found.",
                        "value": {"detail": "Order statuses not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_STATUS_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_STATUS_NOT_FOUND_RESPONSE,
}
