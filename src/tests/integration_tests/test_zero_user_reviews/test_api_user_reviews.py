import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_order_status_not_authenticated(ac):
    response = await ac.post(
        "/orders",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_creating_shopping_cart_items_with_user(ac):
    response = await ac.post(
        "/auth/login",
        data={
            "username": "user12345@example.com",
            "password": "string",
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    assert response.status_code == 204

    ac.headers["Cookie"] = (
        f"ecommerce_token=" f"{ac.cookies['ecommerce_token']}"
    )

    response = await ac.get(
        "/shopping_carts",
    )

    assert response.status_code == 200

    shopping_cart_id = response.json()["id"]

    response = await ac.get(
        "/products/items",
    )

    product_item_id = response.json()["product_items"][0]["id"]

    assert response.status_code == 200

    response = await ac.post(
        f"/shopping_carts/{shopping_cart_id}/items",
        json={"product_item_id": product_item_id},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_order(ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        data={
            "username": "user12345@example.com",
            "password": "string",
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    assert response.status_code == 204

    ac.headers["Cookie"] = (
        f"ecommerce_token=" f"{ac.cookies['ecommerce_token']}"
    )

    response = await ac.get(
        "/payments/methods",
    )
    assert response.status_code == 200

    payment_method_id = response.json()["payment_methods"][0]["id"]

    response = await ac.get(
        "/addresses",
    )
    assert response.status_code == 200

    shipping_address_id = response.json()["addresses"][0]["id"]

    response = await ac.get(
        "/shipping_methods",
    )

    shipping_method_id = response.json()["shipping_methods"][0]["id"]

    order_data = {
        "payment_method_id": payment_method_id,
        "shipping_address_id": shipping_address_id,
        "shipping_method_id": shipping_method_id,
    }

    response = await ac.post(
        "/orders",
        json=order_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_order_(ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        data={
            "username": "user12345@example.com",
            "password": "string",
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    assert response.status_code == 204

    ac.headers["Cookie"] = (
        f"ecommerce_token=" f"{ac.cookies['ecommerce_token']}"
    )

    response = await ac.get("/orders")

    assert response.status_code == 200

    product_categories = response.json()["shop_orders"]

    assert len(product_categories) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "rating_value,comment,status_code",
    [
        (-9, "", 422),
        (10, "", 422),
        (3, "", 200),
        (3, "Wow!", 422),
    ],
)
async def test_create_review(
    ac: AsyncClient, rating_value, comment, status_code
):
    response = await ac.post(
        "/auth/login",
        data={
            "username": "user12345@example.com",
            "password": "string",
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    assert response.status_code == 204

    ac.headers["Cookie"] = (
        f"ecommerce_token=" f"{ac.cookies['ecommerce_token']}"
    )

    response = await ac.get("/orders")

    assert response.status_code == 200

    order_id = response.json()["shop_orders"][0]["id"]

    response = await ac.get(f"/orders/{order_id}/lines")
    assert response.status_code == 200

    order_line_id = response.json()["products_in_order"][0]["id"]

    user_review_data = {
        "ordered_product_id": order_line_id,
        "rating_value": rating_value,
        "comment": comment,
    }

    response = await ac.post(
        "/users/reviews",
        json=user_review_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_get_order_status(ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        data={
            "username": "user12345@example.com",
            "password": "string",
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    assert response.status_code == 204

    ac.headers["Cookie"] = (
        f"ecommerce_token=" f"{ac.cookies['ecommerce_token']}"
    )

    response = await ac.get("/users/reviews")
    assert response.status_code == 200

    user_reviews = response.json()["user_reviews"]
    assert len(user_reviews) == 1
    assert user_reviews[0]["rating_value"] == 3


@pytest.mark.asyncio
async def test_change_order(admin_ac: AsyncClient, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        data={
            "username": "user12345@example.com",
            "password": "string",
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    assert response.status_code == 204

    ac.headers["Cookie"] = (
        f"ecommerce_token=" f"{ac.cookies['ecommerce_token']}"
    )

    response = await ac.get("/users/reviews")
    assert response.status_code == 200

    user_review_id = response.json()["user_reviews"][0]["id"]

    new_order_data = {"comment": "Amazing!", "rating_value": 4}

    response = await ac.patch(
        f"/users/reviews/{user_review_id}",
        json=new_order_data,
    )

    assert response.status_code == 200
    assert response.json()["rating_value"] == 4
    assert response.json()["comment"] == "Amazing!"


@pytest.mark.asyncio
async def test_delete_product_order_status(ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        data={
            "username": "user12345@example.com",
            "password": "string",
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    assert response.status_code == 204

    ac.headers["Cookie"] = (
        f"ecommerce_token=" f"{ac.cookies['ecommerce_token']}"
    )

    response = await ac.get("/users/reviews")
    assert len(response.json()["user_reviews"]) == 1

    user_review_id = response.json()["user_reviews"][0]["id"]

    response = await ac.delete(
        f"/users/reviews/{user_review_id}",
    )
    assert response.status_code == 204

    response = await ac.get("/users/reviews")
    assert response.status_code == 404
