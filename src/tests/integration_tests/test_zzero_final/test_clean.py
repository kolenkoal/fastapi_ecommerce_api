import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_delete_product_item(admin_ac: AsyncClient):
    response = await admin_ac.get("/api/products/items")
    assert response.status_code == 200
    assert len(response.json()["product_items"]) == 2

    product1_id = response.json()["product_items"][0]["id"]
    product2_id = response.json()["product_items"][1]["id"]

    response = await admin_ac.delete(
        f"/api/products/items/{product1_id}",
    )
    assert response.status_code == 204

    response = await admin_ac.delete(
        f"/api/products/items/{product2_id}",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/api/products/items")
    assert response.status_code == 404


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


@pytest.mark.asyncio
async def test_creating_profile_with_user(ac, admin_ac):
    response = await ac.post(
        "/api/auth/login",
        data={
            "email": "user12347890@example.com",
            "password": "string",
        },
    )

    assert response.status_code == 204

    ac.headers["Cookie"] = (
        f"ecommerce_token=" f"{ac.cookies['ecommerce_token']}"
    )

    response = await ac.get(
        "/api/users/me",
    )

    assert response.status_code == 200

    user_id = response.json()["id"]

    response = await admin_ac.delete(
        f"/api/users/{user_id}",
    )

    assert response.status_code == 204
