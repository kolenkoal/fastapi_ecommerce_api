from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.examples import example_variation_option
from src.exceptions import (
    VariationOptionNotFoundException,
    VariationOptionNotImplementedException,
    VariationOptionsNotFoundException,
    raise_http_exception,
)
from src.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_VARIATION_OPTION_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_VARIATION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
    UNAUTHORIZED_FORBIDDEN_VARIATION_OR_OPTION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
    VARIATION_OPTION_NOT_FOUND,
    VARIATION_OPTIONS_NOT_FOUND,
)
from src.users.models import User
from src.variation_options.dao import VariationOptionDAO
from src.variation_options.schemas import (
    SVariationOption,
    SVariationOptionCreate,
    SVariationOptionCreateOptional,
    SVariationOptions,
)


router = APIRouter(prefix="/variation_options", tags=["Variation Options"])


@router.post(
    "",
    # response_model=SVariationOption,
    name="Add variation option to the variation.",
    responses=UNAUTHORIZED_FORBIDDEN_VARIATION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
async def add_variation_option(
    variation_option_data: SVariationOptionCreate = example_variation_option,
    user: User = Depends(current_user),
):
    variation_option = await VariationOptionDAO.add(
        user, variation_option_data
    )

    if not variation_option:
        raise VariationOptionNotImplementedException

    return variation_option


@router.get(
    "",
    name="Get all variation options.",
    response_model=SVariationOptions,
    responses=VARIATION_OPTIONS_NOT_FOUND,
)
async def get_variation_options():
    variation_options = await VariationOptionDAO.find_all()

    if not variation_options:
        raise_http_exception(VariationOptionsNotFoundException)

    return {"variation_options": variation_options}


@router.get(
    "/{variation_option_id}",
    name="Get certain variation option.",
    response_model=SVariationOption,
    responses=VARIATION_OPTION_NOT_FOUND,
)
async def get_variation_option(variation_option_id: UUID):
    variation_option = await VariationOptionDAO.find_by_id(variation_option_id)

    if not variation_option:
        raise_http_exception(VariationOptionNotFoundException)

    return variation_option


@router.patch(
    "/{variation_option_id}",
    response_model=SVariationOptionCreateOptional,
    response_model_exclude_none=True,
    name="Change certain variation.",
    responses=UNAUTHORIZED_FORBIDDEN_VARIATION_OR_OPTION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
async def change_variation_option(
    variation_option_id: UUID,
    data: SVariationOptionCreateOptional,
    user: User = Depends(current_user),
):
    variation_option = await VariationOptionDAO.change(
        variation_option_id, user, data
    )

    if not variation_option:
        raise VariationOptionNotFoundException

    return variation_option


@router.delete(
    "/{variation_option_id}",
    name="Delete certain variation.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_VARIATION_OPTION_NOT_FOUND_RESPONSE,
)
async def delete_variation(
    variation_option_id: UUID,
    user: User = Depends(current_user),
):
    variation_option = await VariationOptionDAO.delete(
        user, variation_option_id
    )

    if not variation_option:
        return {"detail": "The variation option was deleted."}
