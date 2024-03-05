from datetime import date, timedelta

import pytest
from httpx import AsyncClient


@pytest.fixture
async def authenticated_ac_with_payment_types(authenticated_ac):
    response = await authenticated_ac.get("/api/payments/types")
    assert response.status_code == 200
    return authenticated_ac, response.json()[0]["id"]


def create_payment_data(
    payment_type_id, provider, account_number, expiry_date, is_default
):
    return {
        "payment_type_id": payment_type_id,
        "provider": provider,
        "account_number": account_number,
        "expiry_date": expiry_date,
        "is_default": is_default,
    }


@pytest.mark.asyncio
async def test_create_payment_method_not_authenticated(ac):
    payment_method_data = create_payment_data(
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "string",
        "string",
        "2024-02-09",
        True,
    )
    response = await ac.post("/api/payments/methods", json=payment_method_data)
    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "provider,account_number,expiry_date,is_default,status_code",
    [
        ("", "", "", "", 422),
        (
            "47",
            "1111111111111111",
            str(date.today() + timedelta(days=1)),
            "True",
            422,
        ),
        (
            "Master Card",
            "Hi!",
            str(date.today() + timedelta(days=1)),
            "True",
            422,
        ),
        ("Master Card", "1111111111111111", "2023-12-31", "True", 422),
        (
            "Master Card",
            "1111111111111111",
            str(date.today() + timedelta(days=1)),
            "Like",
            422,
        ),
    ],
)
async def test_create_payment_method_with_bad_entities(
    authenticated_ac_with_payment_types,
    authenticated_ac,
    provider,
    account_number,
    expiry_date,
    is_default,
    status_code,
):
    authenticated_ac, payment_type_id = authenticated_ac_with_payment_types
    payment_method_data = create_payment_data(
        payment_type_id, provider, account_number, expiry_date, is_default
    )
    response = await authenticated_ac.post(
        "/api/payments/methods", json=payment_method_data
    )
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_create_payment_method(
    authenticated_ac_with_payment_types, authenticated_ac
):
    authenticated_ac, payment_type_id = authenticated_ac_with_payment_types
    payment_method_data = create_payment_data(
        payment_type_id,
        "Master Card",
        "1111111111111111",
        str(date.today() + timedelta(days=1)),
        True,
    )
    response = await authenticated_ac.post(
        "/api/payments/methods", json=payment_method_data
    )
    assert response.status_code == 200

    response = await authenticated_ac.post(
        "/api/payments/methods", json=payment_method_data
    )
    assert response.status_code == 422


@pytest.fixture
def payment_method_data_fixture(authenticated_ac_with_payment_types):
    authenticated_ac, payment_type_id = authenticated_ac_with_payment_types
    return create_payment_data(
        payment_type_id,
        "MasterCard",
        "1234567812345678",
        str(date.today() + timedelta(days=1)),
        False,
    )


@pytest.mark.asyncio
async def test_get_payment_methods(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/api/payments/methods")
    assert response.status_code == 200
    payment_methods = response.json()["payment_methods"]
    assert len(payment_methods) == 1
    assert payment_methods[0]["account_number"] == "1111111111111111"


@pytest.mark.asyncio
async def test_get_payment_method(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/api/payments/methods")
    assert response.status_code == 200
    payment_method_id = response.json()["payment_methods"][0]["id"]
    response = await authenticated_ac.get(
        f"/api/payments/methods/{payment_method_id}"
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_payment_method(
    authenticated_ac: AsyncClient, payment_method_data_fixture
):
    response = await authenticated_ac.get("/api/payments/methods")
    assert response.status_code == 200
    payment_method_id = response.json()["payment_methods"][0]["id"]
    response = await authenticated_ac.get(
        f"/api/payments/methods/{payment_method_id}"
    )
    assert response.status_code == 200
    payment_method = response.json()
    assert payment_method["provider"] != "Visa"
    assert payment_method["account_number"] != "1234567812345678"
    payment_method_data = {
        "provider": "Visa",
        "account_number": "1234567812345678",
    }
    response = await authenticated_ac.patch(
        f"/api/payments/methods/{payment_method_id}", json=payment_method_data
    )
    new_payment_method_data = response.json()
    assert response.status_code == 200
    assert new_payment_method_data["provider"] == "Visa"
    assert new_payment_method_data["account_number"] == "1234567812345678"


@pytest.mark.asyncio
async def test_delete_payment_method(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/api/payments/methods")
    assert response.status_code == 200
    payment_method_id = response.json()["payment_methods"][0]["id"]
    response = await authenticated_ac.get(
        f"/api/payments/methods/{payment_method_id}"
    )
    assert response.status_code == 200
    response = await authenticated_ac.delete(
        f"/api/payments/methods/{payment_method_id}"
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_create_several_payment_methods(
    authenticated_ac_with_payment_types, authenticated_ac
):
    authenticated_ac, payment_type_id = authenticated_ac_with_payment_types
    payment_data_visa = create_payment_data(
        payment_type_id,
        "Visa",
        "1234567812345678",
        str(date.today() + timedelta(days=1)),
        "True",
    )
    payment_data_master_card = create_payment_data(
        payment_type_id,
        "MasterCard",
        "1234567812345679",
        str(date.today() + timedelta(days=1)),
        "False",
    )
    response = await authenticated_ac.post(
        "/api/payments/methods", json=payment_data_visa
    )
    assert response.status_code == 200
    response = await authenticated_ac.post(
        "/api/payments/methods", json=payment_data_master_card
    )
    assert response.status_code == 200
