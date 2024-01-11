from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    uuid: UUID
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str
    created_at = datetime
    updated_at: datetime
