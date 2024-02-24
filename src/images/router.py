import os
import shutil
from uuid import UUID

from fastapi import APIRouter, UploadFile


router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/products")
async def add_product_image(name: str, category_id: int, file: UploadFile):
    im_path = f"src/static/images/products/{name}_{category_id}.webp"

    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return f"{name}_{category_id}.webp"


@router.delete("/products")
async def delete_products_file(name: str, category_id: int):
    im_path = f"src/static/images/products/{name}_{category_id}.webp"

    if os.path.exists(im_path):
        os.remove(im_path)
        return True
    return False


@router.patch("/products")
async def rename_product_image_file(
    old_name: str, old_category: int, new_name: str, new_category: int
):
    old_path = f"src/static/images/products/{old_name}_{old_category}.webp"
    new_path = f"src/static/images/products/{new_name}_{new_category}.webp"

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return f"{new_name}_{new_category}.webp"
    return None


@router.post("/products/items")
async def add_product_item_image(SKU, product_id: UUID, file: UploadFile):
    im_path = f"src/static/images/products/items/{SKU}_{product_id}.webp"

    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return f"{SKU}_{product_id}.webp"


@router.patch("/products/items")
async def rename_product_item_image_file(
    old_SKU: str,
    old_product: UUID,
    new_SKU: str,
    new_product: UUID,
):
    old_path = f"src/static/images/products/items/{old_SKU}_{old_product}.webp"
    new_path = f"src/static/images/products/items/{new_SKU}_{new_product}.webp"

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return f"{new_SKU}_{new_product}.webp"
    return None


@router.delete("/products/items")
async def delete_product_item_file(SKU: str, product_id: UUID):
    im_path = f"src/static/images/products/items/{SKU}_{product_id}.webp"

    if os.path.exists(im_path):
        os.remove(im_path)
        return True
    return False


@router.post("/profiles")
async def add_profile_image(name: str, file: UploadFile):
    im_path = f"src/static/images/user_profiles/{name}"

    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return name
