from fastapi import status

from src.responses import UNAUTHORIZED_RESPONSE, UNPROCESSABLE_ENTITY


COUNTRY_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Country not found.": {
                        "summary": "Country not found.",
                        "value": {"detail": "Country not found."},
                    },
                }
            }
        }
    }
}

UNAUTHORIZED_COUNTRY_NOT_FOUND_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **COUNTRY_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}
