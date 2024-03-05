from fastapi import status

from src.exceptions import EcommerceException


class OrderStatusesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order Statuses not found."


class OrderStatusNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order Status not found."


class OrderStatusAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such order status already exists."


class OrderStatusNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add order status."
