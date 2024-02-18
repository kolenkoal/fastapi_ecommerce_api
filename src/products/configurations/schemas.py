import uuid
from typing import Optional

from pydantic import BaseModel


class SProductConfiguration(BaseModel):
    product_item_id: uuid.UUID
    variation_option_id: uuid.UUID


class SProductConfigurationOptional(BaseModel):
    product_item_id: Optional[uuid.UUID]
    variation_option_id: Optional[uuid.UUID]


class SProductConfigurations(BaseModel):
    product_configurations: list[SProductConfiguration]
