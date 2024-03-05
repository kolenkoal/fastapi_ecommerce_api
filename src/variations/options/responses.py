from fastapi import status

from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    UNPROCESSABLE_ENTITY,
)
from src.variations.responses import VARIATION_NOT_FOUND


VARIATION_OPTION_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Variation option not found.": {
                        "summary": "Variation option not found.",
                        "value": {"detail": "Variation option not found."},
                    },
                }
            }
        }
    },
}

VARIATION_OPTIONS_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Variation options not found.": {
                        "summary": "Variation options not found.",
                        "value": {"detail": "Variation options not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_VARIATION_OR_OPTION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **VARIATION_OPTION_NOT_FOUND,
    **VARIATION_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_FORBIDDEN_VARIATION_OPTION_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **VARIATION_OPTION_NOT_FOUND,
}
