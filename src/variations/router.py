from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.examples import example_variation
from src.exceptions import VariationNotImplementedException
from src.responses import (
    UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
from src.users.models import User
from src.variations.dao import VariationDAO
from src.variations.schemas import SVariation, SVariationCreate


router = APIRouter(prefix="/variations", tags=["Variations"])


@router.post(
    "",
    response_model=SVariation,
    name="Add variation to the category.",
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
async def add_variation(
    variation_data: SVariationCreate = example_variation,
    user: User = Depends(current_user),
):
    variation = await VariationDAO.add(user, variation_data)

    if not variation:
        raise VariationNotImplementedException

    return variation
