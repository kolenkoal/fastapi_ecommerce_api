from fastapi import status

from src.exceptions import EcommerceException


class OrderNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order not found."


class OrdersNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Orders not found."


class OrderAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such order already exists."


class OrderNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add order."
