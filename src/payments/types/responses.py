from fastapi import status


PAYMENT_TYPES_SUCCESS_EXAMPLE = {
    status.HTTP_200_OK: {
        "content": {
            "application/json": {
                "example": [
                    {
                        "name": "Credit card",
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                    },
                ]
            }
        },
    },
}

PAYMENT_TYPES_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Payment types not found.": {
                        "summary": "Payment types not found.",
                        "value": {"detail": "Payment types not found."},
                    },
                }
            }
        }
    },
}

PAYMENT_TYPES_SUCCESS_NOT_FOUND_RESPONSE = {
    **PAYMENT_TYPES_SUCCESS_EXAMPLE,
    **PAYMENT_TYPES_NOT_FOUND_RESPONSE,
}
