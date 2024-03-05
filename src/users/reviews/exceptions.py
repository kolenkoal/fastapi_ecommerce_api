from fastapi import status

from src.exceptions import EcommerceException


class UserReviewNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User Review not found."


class UserReviewsNotFoundException(EcommerceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User Reviews not found."


class UserReviewAlreadyExistsException(EcommerceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "You already have this product reviewed."


class UserReviewNotImplementedException(EcommerceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add review."
