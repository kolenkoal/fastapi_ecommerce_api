from fastapi import status

from src.responses import FORBIDDEN_RESPONSE, UNAUTHORIZED_RESPONSE


ORDER_LINE_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Order line not found.": {
                        "summary": "Order line not found.",
                        "value": {"detail": "Order line not found."},
                    },
                }
            }
        }
    },
}

ORDER_LINES_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Order lines not found.": {
                        "summary": "Order lines not found.",
                        "value": {"detail": "Order lines not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_ORDER_LINES_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_LINES_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_ORDER_LINE_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_LINE_NOT_FOUND_RESPONSE,
}
