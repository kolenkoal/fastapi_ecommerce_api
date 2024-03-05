from fastapi import status

from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    UNPROCESSABLE_ENTITY,
)


SHOPPING_CART_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shopping cart not found.": {
                        "summary": "Shopping cart not found.",
                        "value": {"detail": "Shopping cart not found."},
                    },
                }
            }
        }
    },
}

SHOPPING_CARTS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shopping carts not found.": {
                        "summary": "Shopping carts not found.",
                        "value": {"detail": "Shopping carts not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_CARTS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHOPPING_CARTS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_CART_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHOPPING_CART_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_FORBIDDEN_CART_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHOPPING_CART_NOT_FOUND_RESPONSE,
}
