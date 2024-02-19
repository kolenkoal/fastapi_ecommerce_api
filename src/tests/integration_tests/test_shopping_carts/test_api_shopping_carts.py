import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_shopping_cart_not_authenticated(ac):
    shopping_cart_data = {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }

    response = await ac.post(
        "/shopping_carts",
        json=shopping_cart_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_creating_shopping_cart_with_user(admin_ac):
    user_data = {
        "email": "user1234@example.com",
        "password": "string",
        "first_name": "string",
        "last_name": "string",
    }
    response = await admin_ac.post(
        "/auth/register",
        json=user_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 201

    user_id = response.json()["id"]

    response = await admin_ac.get(
        "/shopping_carts",
    )

    assert response.status_code == 200

    shopping_carts = response.json()["shopping_carts"]

    assert any(cart["user_id"] == user_id for cart in shopping_carts)


@pytest.mark.asyncio
async def test_get_user_product_categories(admin_ac: AsyncClient):
    response = await admin_ac.get("/shopping_carts")

    assert response.status_code == 200

    shopping_carts = response.json()["shopping_carts"]

    assert len(shopping_carts) == 1


@pytest.mark.asyncio
async def test_get_shopping_cart(admin_ac: AsyncClient):
    response = await admin_ac.get("/shopping_carts")

    assert response.status_code == 200

    shopping_cart_id = response.json()["shopping_carts"][0]["id"]

    response = await admin_ac.get(f"/shopping_carts/{shopping_cart_id}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_shopping_cart(admin_ac: AsyncClient):
    response = await admin_ac.get("/shopping_carts")

    assert response.status_code == 200

    shopping_cart_id = response.json()["shopping_carts"][0]["id"]

    new_shopping_cart_data = {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }
    response = await admin_ac.patch(
        f"/products/categories/{shopping_cart_id}",
        json=new_shopping_cart_data,
    )

    assert response.status_code == 422

    user1_data = {
        "email": "user12345@example.com",
        "password": "string",
        "first_name": "string",
        "last_name": "string",
    }
    response = await admin_ac.post(
        "/auth/register",
        json=user1_data,
        headers={"Content-Type": "application/json"},
    )

    user_id = response.json()["id"]

    new_shopping_cart_data = {"user_id": user_id}

    response = await admin_ac.patch(
        f"/shopping_carts/{shopping_cart_id}",
        json=new_shopping_cart_data,
    )

    assert response.status_code == 422


#
@pytest.mark.asyncio
async def test_delete_shopping_cart(admin_ac: AsyncClient):
    response = await admin_ac.get("/shopping_carts")

    assert response.status_code == 200

    shopping_cart_id = response.json()["shopping_carts"][0]["id"]

    response = await admin_ac.delete(
        f"/shopping_carts/{shopping_cart_id}",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/shopping_carts")
    assert response.status_code == 200
    assert len(response.json()) == 1
