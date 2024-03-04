from fastapi import status

from src.exceptions import EcommerceException


class PaymentTypesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment types not found."


class PaymentTypeNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment type not found."


class WrongPaymentTypeNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid payment type name."
