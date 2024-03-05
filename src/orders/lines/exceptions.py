from fastapi import status

from src.exceptions import EcommerceException


class OrderLineNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order Line not found."


class OrderLinesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order Lines not found."
