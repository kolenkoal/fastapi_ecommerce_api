from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from fastapi import Form, UploadFile
from pydantic import BaseModel

from src.products.categories.schemas import SProductCategory


class SProductCreate(BaseModel):
    name: str
    description: str
    category_id: int


class SProductCreateOptional(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


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


class SProducts(BaseModel):
    products: list[SProduct]


class SProductWithCategory(BaseModel):
    id: UUID
    name: str
    description: str
    product_image: str
    category: SProductCategory
