import shutil

from fastapi import APIRouter, UploadFile


router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/products")
async def add_product_image(name: str, category_id: int, file: UploadFile):
    im_path = f"src/static/images/{name}_{category_id}.webp"

    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return f"{name}_{category_id}.webp"
