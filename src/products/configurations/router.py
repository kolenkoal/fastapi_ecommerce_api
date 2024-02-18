from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.auth.auth import current_user
from src.exceptions import (
    ProductConfigurationNotImplementedException,
    ProductConfigurationsNotFoundException,
    raise_http_exception,
)
from src.products.configurations.dao import ProductConfigurationDAO
from src.products.configurations.schemas import (
    SProductConfiguration,
    SProductConfigurations,
)
from src.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_CONFIGURATION_NOT_FOUND_RESPONSE,
    PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
from src.users.models import User


router = APIRouter(prefix="/configurations")


@router.post(
    "",
    name="Create a product configuration.",
    response_model=SProductConfiguration,
    responses=UNAUTHORIZED_FORBIDDEN_PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE_UNPROCESSABLE_ENTITY,
)
async def create_product_configuration(
    configuration_data: Annotated[SProductConfiguration, Depends()],
    user: User = Depends(current_user),
):
    product_configuration = await ProductConfigurationDAO.add(
        user, configuration_data
    )

    if not product_configuration:
        raise raise_http_exception(ProductConfigurationNotImplementedException)

    return product_configuration


@router.get(
    "",
    name="Get all product configurations.",
    response_model=SProductConfigurations,
    responses=PRODUCT_ITEM_OR_VARIATION_OPTION_NOT_FOUND_RESPONSE,
)
async def get_product_configurations():
    product_configurations = await ProductConfigurationDAO.find_all()

    if not product_configurations:
        raise_http_exception(ProductConfigurationsNotFoundException)

    return {"product_configurations": product_configurations}


@router.delete(
    "",
    name="Delete certain product configuration.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_PRODUCT_CONFIGURATION_NOT_FOUND_RESPONSE,
)
async def delete_variation(
    configuration_data: Annotated[SProductConfiguration, Depends()],
    user: User = Depends(current_user),
):
    product_configuration = await ProductConfigurationDAO.delete(
        user, configuration_data
    )

    if not product_configuration:
        return {"detail": "The product configuration was deleted."}
