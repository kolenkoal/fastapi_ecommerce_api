from fastapi import status

from src.exceptions import EcommerceException


class VariationOptionNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Variation Option not found."


class VariationOptionsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Variation Options not found."


class VariationOptionAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such variation option already exists."


class WrongVariationOptionNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Variation Option Name."


class VariationOptionNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add variation option."
