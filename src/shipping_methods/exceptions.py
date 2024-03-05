from fastapi import status

from src.exceptions import EcommerceException


class ShippingMethodsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shipping Methods not found."


class ShippingMethodNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shipping Method not found."


class ShippingMethodAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such shipping method already exists."


class ShippingMethodWithNameAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Shipping method with new name already exists."


class ShippingMethodNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add shipping method."
