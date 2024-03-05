from fastapi import status

from src.exceptions import EcommerceException


class ShoppingCartNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shopping Cart not found."


class ShoppingCartsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shopping Carts not found."


class ShoppingCartAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such shopping cart already exists."


class ShoppingCartNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add shopping cart."
