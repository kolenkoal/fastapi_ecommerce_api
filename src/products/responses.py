from fastapi import status

from src.products.categories.responses import PRODUCT_CATEGORY_NOT_FOUND
from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    UNPROCESSABLE_ENTITY,
)


PRODUCT_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Product not found.": {
                        "summary": "Product not found.",
                        "value": {"detail": "Product not found."},
                    },
                }
            }
        }
    },
}

PRODUCTS_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Products not found.": {
                        "summary": "Products not found.",
                        "value": {"detail": "Products not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_CATEGORY_OR_PRODUCT_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
    **PRODUCT_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_NOT_FOUND,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCTS_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCTS_NOT_FOUND,
}
