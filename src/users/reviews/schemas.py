from uuid import UUID

from pydantic import BaseModel, field_validator

from src.exceptions import WrongRatingValueException


class SUserReview(BaseModel):
    id: UUID
    user_id: UUID
    ordered_product_id: UUID
    rating_value: int
    comment: str


class SUserReviewCreate(BaseModel):
    ordered_product_id: UUID
    rating_value: int
    comment: str

    @field_validator("rating_value")
    @classmethod
    def validate_rating_value(cls, value: int):
        if 1 <= value <= 5:
            return value
        raise WrongRatingValueException
