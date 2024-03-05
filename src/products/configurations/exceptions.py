from fastapi import status

from src.exceptions import EcommerceException


class ProductConfigurationNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product Configuration not found."


class ProductConfigurationsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product Configurations not found."


class ProductConfigurationAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such product configuration already exists."


class ProductConfigurationNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add product configuration."
