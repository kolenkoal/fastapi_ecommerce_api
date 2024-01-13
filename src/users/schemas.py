from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    uuid: UUID
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str
    created_at: date
    updated_at: date
