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

SHIPPING_METHOD_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shipping method not found.": {
                        "summary": "Shipping method not found.",
                        "value": {"detail": "Shipping method not found."},
                    },
                }
            }
        }
    },
}

SHIPPING_METHODS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shipping methods not found.": {
                        "summary": "Shipping methods not found.",
                        "value": {"detail": "Shipping methods not found."},
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

CART_NOT_FOUND_RESPONSE = {
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

CARTS_NOT_FOUND_RESPONSE = {
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

SHOPPING_CART_ITEM_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Shopping cart item not found.": {
                        "summary": "Shopping cart item not found.",
                        "value": {"detail": "Shopping cart item not found."},
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
PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE = {
    **PRODUCT_ITEM_NOT_FOUND,
    **VARIATION_OPTION_NOT_FOUND,
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

UNAUTHORIZED_FORBIDDEN_SHIPPING_METHOD_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHIPPING_METHOD_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_STATUS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_CART_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEM_NOT_FOUND,
    **CART_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEMS_NOT_FOUND,
    **CART_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_OR_SHOPPING_CART_ITEM_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEMS_NOT_FOUND,
    **CART_NOT_FOUND_RESPONSE,
    **SHOPPING_CART_ITEM_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_CARTS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **CARTS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE,
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

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_NOT_FOUND,
}

DELETED_UNAUTHORIZED_FORBIDDEN_CART_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **CART_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEMS_OR_CART_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHOPPING_CART_ITEM_NOT_FOUND_RESPONSE,
    **CART_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_CONFIGURATION_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_SHOP_ORDER_NOT_FOUND = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **SHOP_ORDER_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_SHIPPING_METHOD_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **SHIPPING_METHOD_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCTS_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCTS_NOT_FOUND,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEM_NOT_FOUND,
}

DELETED_UNAUTHORIZED_FORBIDDEN_VARIATION_OPTION_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **VARIATION_OPTION_NOT_FOUND,
}

UNAUTHORIZED_FORBIDDEN_CART_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **CART_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_NOT_FOUND_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}
UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEM_NOT_FOUND,
    **VARIATION_OPTION_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_PRODUCT_ITEM_ORDER_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **PRODUCT_ITEM_NOT_FOUND,
    **ORDER_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}
