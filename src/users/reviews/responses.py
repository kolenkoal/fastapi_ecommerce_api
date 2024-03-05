from fastapi import status

from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)


USER_REVIEW_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "User review not found.": {
                        "summary": "User review not found.",
                        "value": {"detail": "User review not found."},
                    },
                }
            }
        }
    },
}

USER_REVIEWS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "User reviews not found.": {
                        "summary": "User reviews not found.",
                        "value": {"detail": "User reviews not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_USER_REVIEWS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **USER_REVIEWS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_USER_REVIEW_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **USER_REVIEW_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_USER_REVIEW_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **USER_REVIEW_NOT_FOUND_RESPONSE,
}
