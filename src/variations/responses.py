from fastapi import status

from src.products.categories.responses import PRODUCT_CATEGORY_NOT_FOUND
from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    UNPROCESSABLE_ENTITY,
)


VARIATION_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Variation not found.": {
                        "summary": "Variation not found.",
                        "value": {"detail": "Variation not found."},
                    },
                }
            }
        }
    },
}

VARIATIONS_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Variations not found.": {
                        "summary": "Variations not found.",
                        "value": {"detail": "Variations not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_CATEGORY_OR_VARIATION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
    **VARIATION_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_VARIATION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **VARIATION_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_FORBIDDEN_VARIATION_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **VARIATION_NOT_FOUND,
}
