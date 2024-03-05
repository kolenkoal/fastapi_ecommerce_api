from fastapi import status

from src.exceptions import EcommerceException


class ProductNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product not found."


class ProductsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Products not found."


class ProductAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such product already exists."
