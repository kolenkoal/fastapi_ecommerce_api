from dataclasses import dataclass
from uuid import UUID

from fastapi import Form, UploadFile
from pydantic import BaseModel


class SProductCreate(BaseModel):
    name: str
    description: str
    category_id: int


class SProduct(BaseModel):
    id: UUID
    name: str
    description: str
    product_image: str
    category_id: int


@dataclass
class SProductCreateWithFile:
    name: str = Form(...)
    description: str = Form(...)
    category_id: int = Form(...)
    file: UploadFile = Form(...)
