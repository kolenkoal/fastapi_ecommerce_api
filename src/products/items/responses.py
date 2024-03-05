from fastapi import status

from src.orders.responses import ORDER_NOT_FOUND_RESPONSE
from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    UNPROCESSABLE_ENTITY,
)


PRODUCT_ITEM_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Product item not found.": {
                        "summary": "Product item not found.",
                        "value": {"detail": "Product item not found."},
                    },
                }
            }
        }
    },
}

PRODUCT_ITEMS_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Product items not found.": {
                        "summary": "Product items not found.",
                        "value": {"detail": "Product items not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_PRODUCT_ITEM_ORDER_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **PRODUCT_ITEM_NOT_FOUND,
    **ORDER_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEM_NOT_FOUND,
}
