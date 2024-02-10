import uuid
from typing import List, Optional, Type, Union

from pydantic import BaseModel, Field, field_validator

from src.countries.schemas import SCountry
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
from src.users.schemas import UserRead


class SAddressCreate(BaseModel):
    unit_number: str = Field(max_length=20, min_length=1)
    street_number: str = Field(max_length=256, min_length=1)
    address_line1: str = Field(max_length=256, min_length=2)
    address_line2: Optional[str] = ""
    city: str = Field(max_length=256, min_length=2)
    region: str = Field(max_length=256, min_length=2)
    postal_code: str = Field(max_length=256, min_length=2)
    country_id: uuid.UUID

    @field_validator("city", "region", "address_line1")
    @classmethod
    def validate_city_region_address_line(
        cls, value: str
    ) -> Union[str, Type[WrongCityOrRegionException]]:
        if not LETTER_MATCH_PATTERN.match(value):
            raise WrongCityOrRegionException
        value = REMOVE_WHITESPACES(value)

        return value.title()

    @field_validator("address_line2")
    @classmethod
    def validate_address_line2(
        cls, value: str
    ) -> Union[str, Type[WrongCityOrRegionException], None]:
        if not value:
            return None

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
        return value.upper()

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
                "country_id": "95fa574f-9ac1-413e-9ace-5817e4cda634",
            }
        }


class SAddressOptional(BaseModel):
    unit_number: Optional[str] = None
    street_number: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = ""
    city: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    country_id: Optional[uuid.UUID] = None

    @field_validator("city", "region", "address_line1", "address_line2")
    @classmethod
    def validate_address_line2(
        cls, value: str
    ) -> Union[str, Type[WrongCityOrRegionException], None]:
        if not value:
            return None

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
        return value.upper()

    @field_validator("street_number")
    @classmethod
    def validate_street_number(
        cls, value: str
    ) -> Union[str, Type[WrongStreetNumberException]]:
        if not STREET_NUMBER_PATTERN.match(value):
            raise WrongStreetNumberException
        value = REMOVE_WHITESPACES(value)
        return value


class SAddressCountry(BaseModel):
    id: uuid.UUID
    unit_number: str = Field(min_length=1, max_length=20)
    street_number: str = Field(min_length=1, max_length=256)
    address_line1: str = Field(min_length=2, max_length=256)
    address_line2: Optional[str] = ""
    city: str = Field(min_length=2, max_length=256)
    region: str = Field(min_length=2, max_length=256)
    postal_code: str = Field(min_length=2, max_length=256)
    country: SCountry


class SAddress(SAddressCreate):
    id: uuid.UUID

    class ConfigDict:
        response_model_exclude_unset = True


class SAddressesCountry(SAddressCountry):
    is_default: bool


class SUserAddresses(BaseModel):
    user_id: uuid.UUID
    address_id: uuid.UUID
    is_default: bool = False


class SAllUserAddresses(UserRead):
    addresses: List[SAddressesCountry]


class SAllUsersAddresses(BaseModel):
    Users: List[SAllUserAddresses]


class SAddressUser(SAddressesCountry):
    users_living: List[UserRead]
