from datetime import date, timedelta

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_order_status_not_authenticated(ac):
    response = await ac.post(
        "/orders",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_shipping_method(admin_ac):
    shipping_method_data = {
        "name": "Standard",
        "price": "5.99",
    }

    response = await admin_ac.post(
        "/shipping_methods",
        json=shipping_method_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200


@pytest.fixture
async def ac_with_payment_types(ac):
    response = await ac.get("/payments/types")
    assert response.status_code == 200
    return ac, response.json()[0]["id"]


@pytest.mark.asyncio
async def test_create_payment_method(ac_with_payment_types, ac):
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

    ac, payment_type_id = ac_with_payment_types

    payment_method_data = {
        "payment_type_id": payment_type_id,
        "provider": "Master Card",
        "account_number": "1111111111111111",
        "expiry_date": f"{date.today() + timedelta(days=1)}",
        "is_default": True,
    }

    response = await ac.post(
        "/payments/methods",
        json=payment_method_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200

    response = await ac.post(
        "/payments/methods",
        json=payment_method_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


@pytest.fixture
async def ac_with_countries(ac):
    response = await ac.get("/countries")
    assert response.status_code == 200
    return ac, response.json()[0]["id"]


@pytest.mark.asyncio
async def test_create_address(ac_with_countries, ac):
    ac, country_id = ac_with_countries

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

    address_data = {
        "unit_number": "3A",
        "street_number": "54",
        "address_line1": "Clements Rd",
        "address_line2": "North Shore",
        "city": "Boston",
        "region": "MA",
        "postal_code": "12313",
        "country_id": country_id,
    }

    response = await ac.post(
        "/addresses",
        json=address_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200


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

    response = await ac.get("/orders")
    assert response.status_code == 200

    order_id = response.json()["shop_orders"][0]["id"]

    response = await ac.get(f"/orders/{order_id}")
    assert response.status_code == 200


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

    response = await ac.get("/orders")
    assert response.status_code == 200

    order_id = response.json()["shop_orders"][0]["id"]

    new_order_data = {
        "order_status_id": 2,
    }

    response = await admin_ac.patch(
        f"/orders/{order_id}",
        json=new_order_data,
    )

    assert response.status_code == 200
    assert response.json()["order_status_id"] == 2


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

    response = await ac.get("/orders")
    assert len(response.json()["shop_orders"]) == 1

    order_id = response.json()["shop_orders"][0]["id"]

    response = await ac.delete(
        f"/orders/{order_id}",
    )
    assert response.status_code == 204

    response = await ac.get("/orders")
    assert response.status_code == 404
