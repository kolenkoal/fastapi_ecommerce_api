from fastapi import status

from src.exceptions import EcommerceException


class PaymentMethodsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment Methods not found."


class PaymentMethodNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment Method not found."


class PaymentMethodAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "You already have this payment method added."


class WrongAccountNumberException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Account Number."


class ExpiredCardException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Your Card is Expired."


class InvalidCardException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Card number should have 16 digits."


class WrongProviderNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Provider."
