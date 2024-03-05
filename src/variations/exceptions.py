from fastapi import status

from src.exceptions import EcommerceException


class VariationNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Variation not found."


class VariationsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Variations not found."


class VariationAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such variation already exists."


class WrongVariationNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Variation Name."


class VariationNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add variation."
