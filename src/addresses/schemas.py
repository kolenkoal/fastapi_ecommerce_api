import uuid

from pydantic import BaseModel, Field


class SAddressCreate(BaseModel):
    unit_number: int
    street_number: str = Field(max_length=256, min_length=2)
    address_line1: str = Field(max_length=256, min_length=2)
    address_line2: str = Field(max_length=256, min_length=2)
    city: str = Field(max_length=256, min_length=2)
    region: str = Field(max_length=256, min_length=2)
    postal_code: str = Field(max_length=256, min_length=2)
    country_id: uuid.UUID


class SAddress(SAddressCreate):
    id: uuid.UUID
