from fastapi import status

from src.exceptions import EcommerceException


class ProductItemNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product Item not found."


class ProductItemsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product Items not found."


class ProductItemAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such product item already exists."


class QuantityOfProductItemIsMoreThanInStockException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Quantity Of the Product Item is More Than In Stock"


class WrongQuantityException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid format of quantity."


class ProductItemNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add product item."
