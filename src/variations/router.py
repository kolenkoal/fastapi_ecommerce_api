from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.examples import example_variation
from src.exceptions import (
    VariationNotFoundException,
    VariationNotImplementedException,
    VariationsNotFoundException,
    raise_http_exception,
)
from src.products.responses import (
    UNAUTHORIZED_FORBIDDEN_PRODUCT_CATEGORY_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
from src.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_VARIATION_NOT_FOUND_RESPONSE,
    VARIATION_NOT_FOUND,
    VARIATIONS_NOT_FOUND,
)
from src.users.models import User
from src.variations.dao import VariationDAO
from src.variations.responses import (
    UNAUTHORIZED_FORBIDDEN_CATEGORY_OR_VARIATION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
from src.variations.schemas import (
    SVariation,
    SVariationCreate,
    SVariationCreateOptional,
    SVariations,
    SVariationWithCategoryAndOptions,
)


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


@router.get(
    "",
    name="Get all variations.",
    response_model=SVariations,
    responses=VARIATIONS_NOT_FOUND,
)
async def get_variations():
    variations = await VariationDAO.find_all()

    if not variations:
        raise_http_exception(VariationsNotFoundException)

    return {"variations": variations}


@router.get(
    "/{variation_id}",
    name="Get certain variation.",
    response_model=SVariationWithCategoryAndOptions,
    responses=VARIATION_NOT_FOUND,
)
async def get_variation(variation_id: UUID):
    variation = await VariationDAO.find_by_id(variation_id)

    if not variation:
        raise_http_exception(VariationNotFoundException)

    return variation


@router.patch(
    "/{variation_id}",
    response_model=SVariation,
    response_model_exclude_none=True,
    name="Change certain variation.",
    responses=UNAUTHORIZED_FORBIDDEN_CATEGORY_OR_VARIATION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
async def change_variation(
    variation_id: UUID,
    data: SVariationCreateOptional,
    user: User = Depends(current_user),
):
    variation = await VariationDAO.change(variation_id, user, data)

    if not variation:
        raise VariationNotFoundException

    return variation


@router.delete(
    "/{variation_id}",
    name="Delete certain variation.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_VARIATION_NOT_FOUND_RESPONSE,
)
async def delete_variation(
    variation_id: UUID,
    user: User = Depends(current_user),
):
    variation = await VariationDAO.delete(user, variation_id)

    if not variation:
        return {"detail": "The variation was deleted."}
