from fastapi import status


DELETED_RESPONSE = {
    status.HTTP_204_NO_CONTENT: {
        "content": {
            "application/json": {
                "examples": {
                    "The item was deleted.": {
                        "summary": "The item was deleted.",
                        "value": {"detail": "The item was deleted."},
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

UNPROCESSABLE_ENTITY = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "content": {
            "application/json": {
                "examples": {
                    "You already have this item added.": {
                        "summary": "You already have this item added.",
                        "value": {
                            "detail": "You already have this item added."
                        },
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_FORBIDDEN_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
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

UNAUTHORIZED_FORBIDDEN_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_FORBIDDEN_USER_REVIEW_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **USER_REVIEW_NOT_FOUND_RESPONSE,
}
