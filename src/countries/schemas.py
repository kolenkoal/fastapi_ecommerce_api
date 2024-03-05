import uuid
from typing import List

import pycountry
from pydantic import BaseModel, field_validator

from src.countries.exceptions import WrongCountryNameException
from src.patterns import LETTER_MATCH_PATTERN


class SCountryCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str):
        if not LETTER_MATCH_PATTERN.match(name):
            raise WrongCountryNameException

        if len(name) == 2 and not pycountry.countries.get(alpha_2=name):
            raise WrongCountryNameException

        if len(name) == 3 and not pycountry.countries.get(alpha_3=name):
            raise WrongCountryNameException

        country = pycountry.countries.get(name=name)

        if not country:
            raise WrongCountryNameException

        return country.name.title()


class SCountry(SCountryCreate):
    id: uuid.UUID


class SCountries(BaseModel):
    countries: List[SCountry]
