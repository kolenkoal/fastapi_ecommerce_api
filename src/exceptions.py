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


class UserProfileNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User profile not found."


class CountriesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Countries not found."


class CountryNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Country not found."


class UserReviewNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User Review not found."


class UserReviewsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User Reviews not found."


class ShippingMethodsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shipping Methods not found."


class ShippingMethodNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shipping Method not found."


class OrderStatusesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order Statuses not found."


class OrderStatusNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order Status not found."


class ShoppingCartNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shopping Cart not found."


class ShoppingCartsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shopping Carts not found."


class ShoppingCartItemNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shopping Cart Item not found."


class ShoppingCartItemsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shopping Cart Items not found."


class ShopOrderNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shop Order not found."


class ShopOrdersNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Shop Orders not found."


class OrderLineNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order Line not found."


class OrderLinesNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order Lines not found."


class WrongNameOrSurnameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid First Name or Last Name."


class WrongCountryNameException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid country name."


class WrongRatingValueException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Rating value must be from 1 to 5."


class WrongUnitOrPostalCodeException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Unit number or postal code."


class WrongStreetNumberException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid street number."


class UserReviewAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "You already have this product reviewed."


class ShippingMethodAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such shipping method already exists."


class ShopOrderAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such shop order already exists."


class OrderStatusAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such order status already exists."


class ShippingMethodWithNameAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Shipping method with new name already exists."


class UserAlreadyHasCartException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "User already has a cart."


class UserAlreadyHasProfileException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "User already has a profile."


class UserDoesNotHaveCartException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User does not have a cart."


class ShoppingCartAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Such shopping cart already exists."


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


class QuantityLessThanOneException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Quantity should be at least one."


class WrongAccountNumberException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid Account Number."


class ExpiredCardException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Your Card is Expired."


class InvalidCardException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Card number should have 16 digits."


class ShoppingCartNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add shopping cart."


class UserProfileNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add user profile."


class ShoppingCartItemNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add shopping cart item."


class ShippingMethodNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add shipping method."


class OrderStatusNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add order status."


class ShopOrderNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add shop order."


class UserReviewNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add review."
