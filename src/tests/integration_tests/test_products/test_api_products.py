import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product_not_authenticated(ac):
    product_data = {"name": "Nike Joggers", "category_id": 1}

    response = await ac.post(
        "/api/products",
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
        "/api/products/categories",
        json=product_category_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_create_product(admin_ac, temp_products_file):
    test_name = "Test Product"
    test_description = "Test Description"
    test_category_id = 3

    form_data = {
        "name": test_name,
        "description": test_description,
        "category_id": test_category_id,
    }

    with open(temp_products_file, "rb") as file:
        files = {"file": file}
        response = await admin_ac.post(
            "/api/products", files=files, data=form_data
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_products(ac: AsyncClient):
    response = await ac.get("/api/products")
    assert response.status_code == 200

    products = response.json()["products"]

    assert len(products) == 1
    assert products[0]["name"] == "Test Product"


@pytest.mark.asyncio
async def test_get_product(admin_ac: AsyncClient):
    response = await admin_ac.get("/api/products")
    assert response.status_code == 200

    product_id = response.json()["products"][0]["id"]

    response = await admin_ac.get(f"/api/products/{product_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_product(admin_ac: AsyncClient, temp_products_file):
    response = await admin_ac.get("/api/products")
    assert response.status_code == 200

    product_id = response.json()["products"][0]["id"]

    new_product_data = {"name": "Adidas Joggers"}

    response = await admin_ac.patch(
        f"/api/products/{product_id}",
        json=new_product_data,
    )

    assert response.status_code == 200

    assert response.json()["name"] == "Adidas Joggers"


@pytest.mark.asyncio
async def test_delete_product(admin_ac: AsyncClient):
    response = await admin_ac.get("/api/products")
    assert response.status_code == 200
    assert len(response.json()["products"]) == 1

    product_id = response.json()["products"][0]["id"]

    response = await admin_ac.delete(
        f"/api/products/{product_id}",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/api/products")
    assert response.status_code == 404
