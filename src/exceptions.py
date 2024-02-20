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


class CardAlreadyConnectedWithOtherUserException(EcommerceException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Card is already connected to other user."


class UserHasNoAddressesException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "You do not have any addresses."


class NoSuchAddressException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such address."


class VariationNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Variation not found."


class VariationsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Variations not found."


class VariationOptionNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Variation Option not found."


class VariationOptionsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Variation Options not found."


class CountriesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Countries not found."


class ProductCategoryNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product category not found."


class ProductCategoriesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product categories not found."


class ParentCategoryNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Parent category not found."


class ProductNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product not found."


class ProductsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Products not found."


class ProductConfigurationNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product Configuration not found."


class ProductConfigurationsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product Configurations not found."


class CountryNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Country not found."


class CategoryNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Category not found."


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


class ProductItemNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product Item not found."


class ProductItemsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product Items not found."


class ShoppingCartNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shopping Cart not found."


class ShoppingCartsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shopping Carts not found."


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


class WrongCategoryNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid category name."


class UserAlreadyHasThisAddress(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "You already have this address added."


class PaymentMethodAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "You already have this payment method added."


class UserAlreadyHasCartException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "User already has a cart."


class ProductCategoryAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such product category already exists."


class ProductItemAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such product item already exists."


class ProductConfigurationAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such product configuration already exists."


class VariationAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such variation already exists."


class VariationOptionAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such variation option already exists."


class ProductAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such product already exists."


class ShoppingCartAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such shopping cart already exists."


class ProductCategoryParentNotAllowed(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "A category can not be a parent of itself."


class WrongPaymentTypeNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid payment type name."


class WrongProviderNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Provider."


class WrongPriceException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid format of price."


class WrongQuantityException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid format of quantity."


class PriceLessOrEqualZeroException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Price should be more than zero."


class QuantityLessThanZeroException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Quantity should be more than zero."


class WrongVariationNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Variation Name."


class WrongVariationOptionNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Variation Option Name."


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


class ProductCategoryNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add product category."


class VariationNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add variation."


class VariationOptionNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add variation option."


class ProductItemNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add product item."


class ProductConfigurationNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add product configuration."


class ShoppingCartNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add shopping cart."


class ShoppingCartItemNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add shopping cart item."
