import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_shipping_method_not_authenticated(ac):
    response = await ac.post(
        "/shipping_methods",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,price,status_code",
    [
        ("", None, 422),
        ("47", None, 422),
        ("Standard", "Lok", 422),
        ("Standard", 5.99, 200),
    ],
)
async def test_create_shipping_methods(
    admin_ac: AsyncClient, name, price, status_code
):
    shipping_method_data = {
        "name": name,
        "price": price,
    }

    response = await admin_ac.post(
        "/shipping_methods",
        json=shipping_method_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_get_shipping_methods(ac: AsyncClient):
    response = await ac.get("/shipping_methods")

    assert response.status_code == 200

    product_categories = response.json()["shipping_methods"]

    assert len(product_categories) == 1
    assert product_categories[0]["name"] == "Standard"


@pytest.mark.asyncio
async def test_get_shipping_method(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/shipping_methods/1")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "price,status_code",
    [
        (-9, 422),
        (5.99, 200),
        (6.99, 200),
    ],
)
async def test_change_product_shipping_method(
    admin_ac: AsyncClient, price, status_code
):
    new_shipping_method_data = {
        "price": price,
    }

    response = await admin_ac.patch(
        "/shipping_methods/1",
        json=new_shipping_method_data,
    )

    assert response.status_code == status_code

    if status_code == 200:
        assert response.json()["name"] == "Standard"


@pytest.mark.asyncio
async def test_delete_product_shipping_method(admin_ac: AsyncClient):
    response = await admin_ac.get("/shipping_methods")
    assert len(response.json()["shipping_methods"]) == 1

    response = await admin_ac.delete(
        "/shipping_methods/1",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/shipping_methods")
    assert response.status_code == 404
