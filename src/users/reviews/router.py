from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.exceptions import UserReviewNotImplementedException
from src.responses import UNAUTHORIZED_FORBIDDEN_ORDER_LINE_NOT_FOUND
from src.users.models import User
from src.users.reviews.dao import UserReviewDAO
from src.users.reviews.schemas import SUserReview, SUserReviewCreate


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
