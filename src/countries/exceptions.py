from fastapi import status

from src.exceptions import EcommerceException


class CountryNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Country not found."


class CountriesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Countries not found."


class WrongCountryNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid country name."
