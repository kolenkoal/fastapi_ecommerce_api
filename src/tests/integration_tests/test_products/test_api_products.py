import os
import tempfile

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product_not_authenticated(ac):
    product_data = {"name": "Nike Joggers", "category_id": 1}

    response = await ac.post(
        "/products",
        json=product_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    "name,parent_category_id,status_code",
    [
        ("Hi", None, 200),
    ],
)
@pytest.mark.asyncio
async def test_create_product_category(
    admin_ac, name, parent_category_id, status_code
):
    product_category_data = {
        "name": name,
        "parent_category_id": parent_category_id,
    }
    response = await admin_ac.post(
        "/products/categories",
        json=product_category_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_create_product(admin_ac):
    test_name = "Test Product"
    test_description = "Test Description"
    test_category_id = 3

    with tempfile.NamedTemporaryFile(
        suffix=".jpg", prefix="test_product", delete=False
    ) as tmp_file:
        tmp_file.write(b"test_data")
        tmp_file.close()

        form_data = {
            "name": test_name,
            "description": test_description,
            "category_id": test_category_id,
        }

        files = {"file": open(tmp_file.name, "rb")}

        response = await admin_ac.post(
            "/products",
            files=files,
            data=form_data,
        )

        assert response.status_code == 200

    if tmp_file:
        os.unlink(tmp_file.name)


#
@pytest.mark.asyncio
async def test_get_products(ac: AsyncClient):
    response = await ac.get("/products")
    assert response.status_code == 200

    products = response.json()["products"]

    assert len(products) == 1
    assert products[0]["name"] == "Test Product"


@pytest.mark.asyncio
async def test_get_product(admin_ac: AsyncClient):
    response = await admin_ac.get("/products")
    assert response.status_code == 200

    product_id = response.json()["products"][0]["id"]

    response = await admin_ac.get(f"/products/{product_id}")
    assert response.status_code == 200
