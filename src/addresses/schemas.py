import uuid
from typing import Optional, Type, Union

from pydantic import BaseModel, Field, field_validator

from src.exceptions import (
    WrongCityOrRegionException,
    WrongStreetNumberException,
    WrongUnitOrPostalCodeException,
)
from src.patterns import (
    ALPHA_NUMERIC_PATTERN,
    LETTER_MATCH_PATTERN,
    REMOVE_WHITESPACES,
    STREET_NUMBER_PATTERN,
)


class SAddressCreate(BaseModel):
    unit_number: str = Field(max_length=20, min_length=1)
    street_number: str = Field(max_length=256, min_length=2)
    address_line1: str = Field(max_length=256, min_length=2)
    address_line2: Optional[str] = None
    city: str = Field(max_length=256, min_length=2)
    region: str = Field(max_length=256, min_length=2)
    postal_code: str = Field(max_length=256, min_length=2)
    country_id: uuid.UUID

    @field_validator("city", "region", "address_line1", "address_line2")
    @classmethod
    def validate_city_region_address_line(
        cls, value: str
    ) -> Union[str, Type[WrongCityOrRegionException]]:
        if not LETTER_MATCH_PATTERN.match(value):
            raise WrongCityOrRegionException
        value = REMOVE_WHITESPACES(value)

        return value.title()

    @field_validator("postal_code", "unit_number")
    @classmethod
    def validate_postal_code_or_unit_number(
        cls, value: str
    ) -> Union[str, Type[WrongUnitOrPostalCodeException]]:
        if not ALPHA_NUMERIC_PATTERN.match(value):
            raise WrongUnitOrPostalCodeException

        value = REMOVE_WHITESPACES(value)
        return value.title()

    @field_validator("street_number")
    @classmethod
    def validate_street_number(
        cls, value: str
    ) -> Union[str, Type[WrongStreetNumberException]]:
        if not STREET_NUMBER_PATTERN.match(value):
            raise WrongStreetNumberException
        value = REMOVE_WHITESPACES(value)
        return value

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "unit_number": "3A",
                "street_number": "54",
                "address_line1": "Clements Rd",
                "address_line2": "North Shore",
                "city": "Boston",
                "region": "MA",
                "postal_code": "12313",
                "country_id": "300f1712-a311-40da-94e1-acc569588fe9",
            }
        }


class SAddress(SAddressCreate):
    id: uuid.UUID
