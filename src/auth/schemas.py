import re
import uuid
from typing import Type, Union

from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr, Field, field_validator

from src.exceptions import (
    WrongNameOrSurnameException,
    WrongPhoneNumberException,
)


PHONE_MATCH_PATTERN = re.compile(
    r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$"
)
LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserUpdate(schemas.BaseUserUpdate):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str


class UserRead(schemas.CreateUpdateDictModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str = Field(max_length=1024, min_length=2)
    first_name: str = Field(max_length=256, min_length=2)
    last_name: str = Field(max_length=256)
    phone_number: str

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_first_name_or_last_name(
        cls, value: str
    ) -> Union[str, Type[WrongNameOrSurnameException]]:
        if not LETTER_MATCH_PATTERN.match(value):
            return WrongNameOrSurnameException
        return value

    @field_validator("phone_number")
    @classmethod
    def correct_phone_number(
        cls, phone: str
    ) -> Union[Type[WrongPhoneNumberException], str]:
        if not PHONE_MATCH_PATTERN.match(phone):
            return WrongPhoneNumberException
        return phone

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "changeme",
                "first_name": "Jose",
                "last_name": "Clifford",
                "phone_number": "+79169140000",
            }
        }
