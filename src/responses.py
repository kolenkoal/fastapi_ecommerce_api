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

PARENT_CATEGORY_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Parent category not found.": {
                        "summary": "Parent category not found.",
                        "value": {"detail": "Parent category not found."},
                    },
                }
            }
        }
    },
}

PRODUCT_CATEGORY_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Product category not found.": {
                        "summary": "Product category not found.",
                        "value": {"detail": "Product category not found."},
                    },
                }
            }
        }
    },
}

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
PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE = {
    **PRODUCT_ITEM_NOT_FOUND,
    **VARIATION_OPTION_NOT_FOUND,
}

PAYMENT_TYPES_SUCCESS_NOT_FOUND_RESPONSE = {
    **PAYMENT_TYPES_SUCCESS_EXAMPLE,
    **PAYMENT_TYPES_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
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

UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
}

UNAUTHORIZED_FORBIDDEN_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_PAYMENT_METHOD_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PAYMENT_METHOD_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PAYMENT_METHOD_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PAYMENT_METHOD_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
}

DELETED_UNAUTHORIZED_FORBIDDEN_ORDER_STATUS_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_STATUS_NOT_FOUND_RESPONSE,
}

DELETED_UNAUTHORIZED_FORBIDDEN_VARIATION_NOT_FOUND_RESPONSE = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **VARIATION_NOT_FOUND,
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

UNAUTHORIZED_COUNTRY_NOT_FOUND_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **COUNTRY_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_PARENT_CATEGORY_NOT_FOUND_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PARENT_CATEGORY_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
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

UNAUTHORIZED_PARENT_CATEGORY_NOT_FOUND_UNPROCESSABLE_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **PARENT_CATEGORY_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}
UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_ITEM_NOT_FOUND,
    **VARIATION_OPTION_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_VARIATION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **VARIATION_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_CATEGORY_OR_VARIATION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
    **VARIATION_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_CATEGORY_OR_PRODUCT_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **PRODUCT_CATEGORY_NOT_FOUND,
    **PRODUCT_NOT_FOUND,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_FORBIDDEN_VARIATION_OR_OPTION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **VARIATION_OPTION_NOT_FOUND,
    **VARIATION_NOT_FOUND,
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

UNAUTHORIZED_PAYMENT_OR_SHIPPING_METHOD_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **PAYMENT_METHOD_NOT_FOUND_RESPONSE,
    **SHIPPING_METHOD_NOT_FOUND_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

UNAUTHORIZED_PRODUCT_ITEM_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **PRODUCT_ITEM_NOT_FOUND,
    **ORDER_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}
