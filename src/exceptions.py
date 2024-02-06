from fastapi import HTTPException, status


class EcommerceException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


def raise_http_exception(exception_class):
    raise HTTPException(
        status_code=exception_class.status_code, detail=exception_class.detail
    )


class ForbiddenException(EcommerceException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Forbidden"


class UserHasNoAddressesException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "You do not have any addresses."


class NoSuchAddressException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such address."


class CountriesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Countries not found."


class CountryNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Country not found."


class AddressesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Addresses not found."


class AddressNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Address not found."


class DefaultAddressNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "You do not have default address."


class PaymentTypesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment types not found."


class PaymentTypeNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment type not found."


class PaymentMethodNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment Method not found."


class PaymentMethodsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Payment Methods not found."


class WrongNameOrSurnameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid First Name or Last Name."


class WrongCountryNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid country name."


class WrongCityOrRegionException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid City, Region or Address Line."


class WrongUnitOrPostalCodeException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Unit number or postal code."


class WrongStreetNumberException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid street number."


class UserAlreadyHasThisAddress(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "You already have this address added."


class WrongPaymentTypeNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid payment type name."


class WrongProviderNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Provider."


class WrongAccountNumberException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Account Number."


class ExpiredCardException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Your Card is Expired."


class InvalidCardException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Card number should have 16 digits."


class AddressNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add address."
