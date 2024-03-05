from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.exceptions import (
    UserReviewNotFoundException,
    UserReviewNotImplementedException,
    UserReviewsNotFoundException,
    raise_http_exception,
)
from src.orders.lines.responses import (
    UNAUTHORIZED_FORBIDDEN_ORDER_LINE_NOT_FOUND,
)
from src.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_USER_REVIEW_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_USER_REVIEWS_NOT_FOUND_RESPONSE,
)
from src.users.models import User
from src.users.reviews.dao import UserReviewDAO
from src.users.reviews.schemas import (
    SUserReview,
    SUserReviewCreate,
    SUserReviewCreateOptional,
    SUserReviews,
)


router = APIRouter(prefix="/reviews")


@router.post(
    "",
    name="Add a review to the ordered product.",
    response_model=SUserReview,
    responses=UNAUTHORIZED_FORBIDDEN_ORDER_LINE_NOT_FOUND,
)
async def create_review_on_ordered_product(
    review_data: SUserReviewCreate, user: User = Depends(current_user)
):
    user_review = await UserReviewDAO.add(user, review_data)

    if not user_review:
        raise UserReviewNotImplementedException

    return user_review


@router.get(
    "",
    name="Get user reviews.",
    response_model=SUserReviews,
    responses=UNAUTHORIZED_FORBIDDEN_USER_REVIEWS_NOT_FOUND_RESPONSE,
)
async def get_user_reviews(user: User = Depends(current_user)):
    user_reviews = await UserReviewDAO.find_all(user)

    if not user_reviews:
        raise UserReviewsNotFoundException

    return {"user_reviews": user_reviews}


@router.patch(
    "/{user_review_id}",
    response_model=SUserReview,
    name="Change certain user review.",
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_USER_REVIEW_NOT_FOUND_RESPONSE,
)
async def change_shopping_cart_item(
    user_review_id: UUID,
    data: SUserReviewCreateOptional,
    user: User = Depends(current_user),
):
    user_review = await UserReviewDAO.change(user_review_id, user, data)

    if not user_review:
        raise_http_exception(UserReviewNotFoundException)

    return user_review


@router.delete(
    "/{user_review_id}",
    name="Delete certain shopping cart.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_USER_REVIEW_NOT_FOUND_RESPONSE,
)
async def delete_shopping_cart(
    user_review_id: UUID,
    user: User = Depends(current_user),
):
    user_review = await UserReviewDAO.delete(user, user_review_id)

    if not user_review:
        return {"detail": "The user review was deleted."}
