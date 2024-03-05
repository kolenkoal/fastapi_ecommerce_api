from fastapi import status

from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    UNPROCESSABLE_ENTITY,
)


PARENT_CATEGORY_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Parent category not found.": {
                        "summary": "Parent category not found.",
                        "value": {"detail": "Parent category not found."},
                    },
                }
            }
        }
    },
}

PRODUCT_CATEGORY_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Product category not found.": {
                        "summary": "Product category not found.",
                        "value": {"detail": "Product category not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
}

UNAUTHORIZED_FORBIDDEN_PARENT_CATEGORY_NOT_FOUND_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PARENT_CATEGORY_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_PARENT_CATEGORY_NOT_FOUND_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **PARENT_CATEGORY_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
}
