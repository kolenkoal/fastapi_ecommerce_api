import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_shopping_cart_not_authenticated(ac):
    shopping_cart_data = {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }

    response = await ac.post(
        "/api/shopping_carts",
        json=shopping_cart_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_creating_profile_with_user(ac):
    user_data = {
        "email": "user12347890@example.com",
        "password": "string",
        "first_name": "string",
        "last_name": "string",
    }
    response = await ac.post(
        "/api/auth/register",
        json=user_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 201

    user_id = response.json()["id"]

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
        "/api/users/profile",
    )

    assert response.status_code == 200

    user_profile = response.json()
    assert user_profile["user_id"] == user_id
    assert user_profile["profile_image"] == "default.webp"
    assert user_profile["bio"] is None


@pytest.mark.asyncio
async def test_change_profile_bio(ac: AsyncClient):
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

    new_bio = {
        "bio": "I'm cool",
    }

    response = await ac.patch(
        "/api/users/profile/bio",
        json=new_bio,
    )

    assert response.status_code == 200
    assert response.json()["bio"] == "I'm cool"


@pytest.mark.asyncio
async def test_change_profile_image(ac: AsyncClient, temp_products_file):
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

    with open(temp_products_file, "rb") as file:
        files = {"file": file}
        response = await ac.patch("/api/users/profile/image", files=files)
        assert response.status_code == 200

    assert response.status_code == 200
