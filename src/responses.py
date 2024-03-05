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

SHOP_ORDERS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shop orders not found.": {
                        "summary": "Shop orders not found.",
                        "value": {"detail": "Shop orders not found."},
                    },
                }
            }
        }
    },
}

SHOP_ORDER_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shop order not found.": {
                        "summary": "Shop order not found.",
                        "value": {"detail": "Shop order not found."},
                    },
                }
            }
        }
    },
}

ORDER_LINES_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Order lines not found.": {
                        "summary": "Order lines not found.",
                        "value": {"detail": "Order lines not found."},
                    },
                }
            }
        }
    },
}

ORDER_LINE_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Order line not found.": {
                        "summary": "Order line not found.",
                        "value": {"detail": "Order line not found."},
                    },
                }
            }
        }
    },
}

ORDER_STATUS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Order status not found.": {
                        "summary": "Order status not found.",
                        "value": {"detail": "Order status not found."},
                    },
                }
            }
        }
    },
}

ORDER_STATUSES_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Order statuses not found.": {
                        "summary": "Order statuses not found.",
                        "value": {"detail": "Order statuses not found."},
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

ORDER_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shop Order not found.": {
                        "summary": "Shop Order not found.",
                        "value": {"detail": "Shop Order not found."},
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

UNAUTHORIZED_SHOP_ORDERS_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **SHOP_ORDERS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_SHOP_ORDER_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **SHOP_ORDER_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_SHOP_ORDERS_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHOP_ORDERS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_ORDER_LINES_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_LINES_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_ORDER_LINE_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_LINE_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_SHOP_ORDER_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHOP_ORDER_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_STATUS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_STATUS_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_USER_REVIEW_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **USER_REVIEW_NOT_FOUND_RESPONSE,
}
DELETED_UNAUTHORIZED_SHOP_ORDER_NOT_FOUND = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **SHOP_ORDER_NOT_FOUND_RESPONSE,
}
