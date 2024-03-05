from fastapi import status

from src.addresses.responses import ADDRESS_NOT_FOUND_RESPONSE
from src.payments.methods.response import PAYMENT_METHOD_NOT_FOUND_RESPONSE
from src.responses import (
    DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    UNPROCESSABLE_ENTITY,
)
from src.shipping_methods.responses import SHIPPING_METHOD_NOT_FOUND_RESPONSE


ORDER_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Order not found.": {
                        "summary": "Order not found.",
                        "value": {"detail": "Order not found."},
                    },
                }
            }
        }
    },
}

ORDERS_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Orders not found.": {
                        "summary": "Orders not found.",
                        "value": {"detail": "Orders not found."},
                    },
                }
            }
        }
    },
}

UNAUTHORIZED_ORDERS_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **ORDERS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_ORDER_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **ORDER_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_ORDERS_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDERS_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_ORDER_NOT_FOUND = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **ORDER_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_PAYMENT_OR_SHIPPING_METHOD_ADDRESS_NOT_FOUND_UNPROCESSABLE_ENTITY_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **PAYMENT_METHOD_NOT_FOUND_RESPONSE,
    **SHIPPING_METHOD_NOT_FOUND_RESPONSE,
    **ADDRESS_NOT_FOUND_RESPONSE,
    **UNPROCESSABLE_ENTITY,
}

DELETED_UNAUTHORIZED_ORDER_NOT_FOUND = {
    **DELETED_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **ORDER_NOT_FOUND_RESPONSE,
}
