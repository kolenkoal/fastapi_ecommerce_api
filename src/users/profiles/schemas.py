from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SUserProfileCreateOptional(BaseModel):
    bio: Optional[str] = None


class SUserProfile(BaseModel):
    id: UUID
    user_id: UUID
    profile_image: str
    bio: Optional[str]
