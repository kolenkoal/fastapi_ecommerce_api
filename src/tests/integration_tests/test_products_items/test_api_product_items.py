import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product_item_not_authenticated(ac):
    product_item_data = {"name": "Nike Joggers", "category_id": 1}

    response = await ac.post(
        "/api/products/items",
        json=product_item_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


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


@pytest.mark.parametrize(
    "price,quantity_in_stock,status_code",
    [
        ("1.99", 4, 200),
        ("lk", 4, 422),
        ("1.99", "l", 422),
    ],
)
@pytest.mark.asyncio
async def test_create_product_item(
    admin_ac, price, quantity_in_stock, status_code, temp_product_items_file
):
    response = await admin_ac.get("/api/products")
    assert response.status_code == 200

    product_id = response.json()["products"][0]["id"]

    form_data = {
        "price": price,
        "quantity_in_stock": quantity_in_stock,
        "product_id": product_id,
    }

    with open(temp_product_items_file, "rb") as file:
        files = {"file": file}
        response = await admin_ac.post(
            "/api/products/items", files=files, data=form_data
        )
        assert response.status_code == status_code


@pytest.mark.asyncio
async def test_get_product_items(ac: AsyncClient):
    response = await ac.get("/api/products/items")

    assert response.status_code == 200

    product_items = response.json()["product_items"]

    assert len(product_items) == 1
    assert product_items[0]["price"] == "1.99"


#
@pytest.mark.asyncio
async def test_get_product_item(admin_ac: AsyncClient):
    response = await admin_ac.get("/api/products/items")
    assert response.status_code == 200

    product_item_id = response.json()["product_items"][0]["id"]

    response = await admin_ac.get(f"/api/products/items/{product_item_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_product_item(
    admin_ac: AsyncClient, temp_product_items_file
):
    response = await admin_ac.get("/api/products/items")
    assert response.status_code == 200

    product_item_id = response.json()["product_items"][0]["id"]

    new_product_item_data = {"price": "2.99"}

    response = await admin_ac.patch(
        f"/api/products/items/{product_item_id}",
        json=new_product_item_data,
    )

    assert response.status_code == 200

    assert response.json()["price"] == "2.99"


@pytest.mark.asyncio
async def test_delete_product_item(admin_ac: AsyncClient):
    response = await admin_ac.get("/api/products/items")
    assert response.status_code == 200
    assert len(response.json()["product_items"]) == 1

    product_item_id = response.json()["product_items"][0]["id"]

    response = await admin_ac.delete(
        f"/api/products/items/{product_item_id}",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/api/products/items")
    assert response.status_code == 404
