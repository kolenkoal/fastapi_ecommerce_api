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

DELETED_RESPONSE = {
    status.HTTP_204_NO_CONTENT: {
        "content": {
            "application/json": {
                "examples": {
                    "The address was deleted.": {
                        "summary": "The address was deleted.",
                        "value": {"detail": "The address was deleted."},
                    },
                }
            }
        }
    }
}

UNAUTHORIZED_RESPONSE = {
    status.HTTP_401_UNAUTHORIZED: {
        "content": {
            "application/json": {
                "examples": {
                    "Unauthorized.": {
                        "summary": "A user is not authorized.",
                        "value": {"detail": "Unauthorized."},
                    },
                }
            }
        }
    }
}

FORBIDDEN_RESPONSE = {
    status.HTTP_403_FORBIDDEN: {
        "content": {
            "application/json": {
                "examples": {
                    "Forbidden.": {
                        "summary": "Forbidden.",
                        "value": {"detail": "Forbidden."},
                    },
                }
            }
        }
    },
}

ADDRESS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Addresses not found.": {
                        "summary": "Addresses not found.",
                        "value": {"detail": "Addresses not found."},
                    },
                }
            }
        }
    }
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

PAYMENT_METHODS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Payment methods not found.": {
                        "summary": "Payment methods not found.",
                        "value": {"detail": "Payment methods not found."},
                    },
                }
            }
        }
    },
}

PAYMENT_METHOD_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Payment method not found.": {
                        "summary": "Payment method not found.",
                        "value": {"detail": "Payment method not found."},
                    },
                }
            }
        }
    },
}

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

UNPROCESSABLE_ENTITY = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "content": {
            "application/json": {
                "examples": {
                    "You already have this address added.": {
                        "summary": "You already have this address added.",
                        "value": {
                            "detail": "You already have this address added."
                        },
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

UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_PAYMENT_METHOD_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PAYMENT_METHOD_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_COUNTRY_NOT_FOUND_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **COUNTRY_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_ADDRESS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_PAYMENT_METHODS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **PAYMENT_METHODS_NOT_FOUND_RESPONSE,
}
