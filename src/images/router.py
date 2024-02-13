import os
import shutil

from fastapi import APIRouter, UploadFile


router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/products")
async def add_product_image(name: str, category_id: int, file: UploadFile):
    im_path = f"src/static/images/{name}_{category_id}.webp"

    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return f"{name}_{category_id}.webp"


@router.delete("/products")
async def delete_products_file(name: str, category_id: int):
    im_path = f"src/static/images/{name}_{category_id}.webp"

    if os.path.exists(im_path):
        os.remove(im_path)
        return True
    return False


@router.patch("/products")
async def rename_file(
    old_name: str, old_category: int, new_name: str, new_category: int
):
    old_path = f"src/static/images/{old_name}_{old_category}.webp"
    new_path = f"src/static/images/{new_name}_{new_category}.webp"

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return f"{new_name}_{new_category}.webp"
    return None
