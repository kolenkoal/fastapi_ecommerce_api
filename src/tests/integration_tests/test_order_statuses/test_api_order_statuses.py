import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_order_status_not_authenticated(ac):
    response = await ac.post(
        "/orders/statuses",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,status_code",
    [
        ("", 422),
        ("47", 422),
        ("Okay", 200),
        ("Okay", 422),
    ],
)
async def test_create_order_statuses(
    admin_ac: AsyncClient, status, status_code
):
    order_status_data = {
        "status": status,
    }

    response = await admin_ac.post(
        "/orders/statuses",
        json=order_status_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_get_order_statuses(ac: AsyncClient):
    response = await ac.get("/orders/statuses")

    assert response.status_code == 200

    product_categories = response.json()["order_statuses"]

    assert len(product_categories) == 6
    assert product_categories[5]["status"] == "Okay"


@pytest.mark.asyncio
async def test_get_order_status(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/orders/statuses/6")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,status_code",
    [
        ("Okay", 200),
        ("", 422),
        ("4", 422),
        ("Yooo", 200),
    ],
)
async def test_change_product_order_status(
    admin_ac: AsyncClient, status, status_code
):
    new_order_status_data = {
        "status": status,
    }

    response = await admin_ac.patch(
        "/orders/statuses/6",
        json=new_order_status_data,
    )

    assert response.status_code == status_code

    if status_code == 200:
        assert response.json()["status"] == status


@pytest.mark.asyncio
async def test_delete_product_order_status(admin_ac: AsyncClient):
    response = await admin_ac.get("/orders/statuses")
    assert len(response.json()["order_statuses"]) == 6

    response = await admin_ac.delete(
        "/orders/statuses/6",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/orders/statuses")
    assert response.status_code == 200
    assert len(response.json()["order_statuses"]) == 5
