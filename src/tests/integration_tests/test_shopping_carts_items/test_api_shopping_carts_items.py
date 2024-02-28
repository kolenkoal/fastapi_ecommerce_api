import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_shopping_cart_item_not_authenticated(ac):
    response = await ac.post(
        "/api/shopping_carts/3/items",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_product_item(admin_ac, temp_product_items_file):
    response = await admin_ac.get("/api/products")
    assert response.status_code == 200

    product_id = response.json()["products"][0]["id"]

    form_data = {
        "price": "3.99",
        "quantity_in_stock": 2,
        "product_id": product_id,
    }

    with open(temp_product_items_file, "rb") as file:
        files = {"file": file}
        response = await admin_ac.post(
            "/api/products/items", files=files, data=form_data
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_creating_shopping_cart_items_with_user(ac):
    response = await ac.post(
        "/api/auth/login",
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
        "/api/shopping_carts",
    )

    assert response.status_code == 200

    shopping_cart_id = response.json()["id"]

    response = await ac.get(
        "/api/products/items",
    )

    product_item_id = response.json()["product_items"][0]["id"]

    assert response.status_code == 200

    response = await ac.post(
        f"/api/shopping_carts/{shopping_cart_id}/items",
        json={"product_item_id": product_item_id},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_shopping_cart_items(ac: AsyncClient):
    response = await ac.post(
        "/api/auth/login",
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
        "/api/shopping_carts",
    )

    assert response.status_code == 200

    shopping_cart_id = response.json()["id"]

    response = await ac.get(
        f"/api/shopping_carts/{shopping_cart_id}/items",
    )

    assert response.status_code == 200

    shopping_cart_items = response.json()["cart_items"]

    assert len(shopping_cart_items) == 1


@pytest.mark.parametrize(
    "quantity,status_code",
    [
        (1, 200),
        (6, 422),
    ],
)
@pytest.mark.asyncio
async def test_change_shopping_cart(quantity, status_code, ac: AsyncClient):
    response = await ac.post(
        "/api/auth/login",
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
        "/api/shopping_carts",
    )

    assert response.status_code == 200

    shopping_cart_id = response.json()["id"]

    response = await ac.get(
        f"/api/shopping_carts/{shopping_cart_id}/items",
    )

    assert response.status_code == 200

    shopping_cart_items = response.json()["cart_items"]

    assert len(shopping_cart_items) == 1

    product_item_id = shopping_cart_items[0]["id"]

    new_shopping_cart_item_data = {
        "quantity": quantity,
    }
    response = await ac.patch(
        f"/api/shopping_carts/{shopping_cart_id}/items/{product_item_id}",
        json=new_shopping_cart_item_data,
    )

    assert response.status_code == status_code

    if status_code == 200:
        response = await ac.get(
            f"/api/shopping_carts/{shopping_cart_id}/items",
        )

        assert response.status_code == 200

        product_item_quantity = shopping_cart_items[0]["quantity"]

        assert product_item_quantity == quantity


@pytest.mark.asyncio
async def test_delete_shopping_cart_item(ac: AsyncClient):
    response = await ac.post(
        "/api/auth/login",
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
        "/api/shopping_carts",
    )

    assert response.status_code == 200

    shopping_cart_id = response.json()["id"]

    response = await ac.get(
        f"/api/shopping_carts/{shopping_cart_id}/items",
    )

    assert response.status_code == 200

    shopping_cart_items = response.json()["cart_items"]

    assert len(shopping_cart_items) == 1

    product_item_id = shopping_cart_items[0]["id"]

    response = await ac.delete(
        f"/api/shopping_carts/{shopping_cart_id}/items/{product_item_id}",
    )
    assert response.status_code == 204

    response = await ac.get(f"/api/shopping_carts/{shopping_cart_id}/items")
    assert response.status_code == 404
