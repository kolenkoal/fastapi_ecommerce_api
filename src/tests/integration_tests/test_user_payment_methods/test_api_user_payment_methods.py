from datetime import date, timedelta

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user_payment_method_not_authenticated(ac):
    payment_method_data = {
        "payment_type_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "provider": "string",
        "account_number": "string",
        "expiry_date": "2024-02-09",
        "is_default": True,
    }

    response = await ac.post(
        "/payments/methods",
        json=payment_method_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


@pytest.fixture
async def authenticated_ac_with_payment_types(authenticated_ac):
    response = await authenticated_ac.get("/payments/types")
    assert response.status_code == 200
    return authenticated_ac, response.json()[0]["id"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "provider,account_number,expiry_date,is_default,status_code",
    [
        ("", "", "", "", 422),
        (
            "47",
            "1111111111111111",
            f"{date.today() + timedelta(days=1)}",
            "True",
            422,
        ),
        (
            "Master Card",
            "Hi!",
            f"{date.today() + timedelta(days=1)}",
            "True",
            422,
        ),
        ("Master Card", "1111111111111111", "2023-12-31", "True", 422),
        (
            "Master Card",
            "1111111111111111",
            f"{date.today() + timedelta(days=1)}",
            "Like",
            422,
        ),
    ],
)
async def test_create_user_payment_method_with_bad_entities(
    authenticated_ac_with_payment_types,
    authenticated_ac,
    provider,
    account_number,
    expiry_date,
    is_default,
    status_code,
):
    authenticated_ac, payment_type_id = authenticated_ac_with_payment_types
    payment_method_data = {
        "payment_type_id": payment_type_id,
        "provider": provider,
        "account_number": account_number,
        "expiry_date": expiry_date,
        "is_default": is_default,
    }

    response = await authenticated_ac.post(
        "/payments/methods",
        json=payment_method_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_create_payment_method(
    authenticated_ac_with_payment_types, authenticated_ac
):
    authenticated_ac, payment_type_id = authenticated_ac_with_payment_types
    payment_method_data = {
        "payment_type_id": payment_type_id,
        "provider": "Master Card",
        "account_number": "1111111111111111",
        "expiry_date": f"{date.today() + timedelta(days=1)}",
        "is_default": True,
    }

    response = await authenticated_ac.post(
        "/payments/methods",
        json=payment_method_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200

    response = await authenticated_ac.post(
        "/payments/methods",
        json=payment_method_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_user_payment_methods(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/payments/methods")
    assert response.status_code == 200

    payment_methods = response.json()["payment_methods"]

    assert len(payment_methods) == 1
    assert payment_methods[0]["account_number"] == "1111111111111111"


@pytest.mark.asyncio
async def test_get_payment_method(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/payments/methods")
    assert response.status_code == 200

    payment_method_id = response.json()["payment_methods"][0]["id"]
    response = await authenticated_ac.get(
        f"/payments/methods/{payment_method_id}"
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_user_payment_method(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/payments/methods")
    assert response.status_code == 200

    payment_method_id = response.json()["payment_methods"][0]["id"]

    response = await authenticated_ac.get(
        f"/payments/methods/{payment_method_id}"
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
        f"/payments/methods/{payment_method_id}",
        json=payment_method_data,
    )

    new_payment_method_data = response.json()
    assert response.status_code == 200
    assert new_payment_method_data["provider"] == "Visa"
    assert new_payment_method_data["account_number"] == "1234567812345678"


@pytest.mark.asyncio
async def test_delete_user_payment_method(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/payments/methods")
    assert response.status_code == 200

    payment_method_id = response.json()["payment_methods"][0]["id"]

    response = await authenticated_ac.get(
        f"/payments/methods/{payment_method_id}"
    )
    assert response.status_code == 200

    response = await authenticated_ac.delete(
        f"/payments/methods/{payment_method_id}"
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_create_several_payment_methods(
    authenticated_ac_with_payment_types, authenticated_ac
):
    authenticated_ac, payment_type_id = authenticated_ac_with_payment_types

    payment_data_visa = {
        "payment_type_id": payment_type_id,
        "provider": "Visa",
        "account_number": "1234567812345678",
        "expiry_date": f"{date.today() + timedelta(days=1)}",
        "is_default": "True",
    }

    payment_data_master_card = {
        "payment_type_id": payment_type_id,
        "provider": "MasterCard",
        "account_number": "1234567812345679",
        "expiry_date": f"{date.today() + timedelta(days=1)}",
        "is_default": "False",
    }

    response = await authenticated_ac.post(
        "/payments/methods",
        json=payment_data_visa,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200

    response = await authenticated_ac.post(
        "/payments/methods",
        json=payment_data_master_card,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_set_default_payment_method(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/payments/methods")
    payment_methods = response.json()["payment_methods"]

    assert len(payment_methods) == 2

    is_default1 = payment_methods[0]["is_default"]
    payment_method_id_2, is_default2 = (
        payment_methods[1]["id"],
        payment_methods[1]["is_default"],
    )

    assert is_default1
    assert not is_default2

    response = await authenticated_ac.post(
        f"/payments/methods/{payment_method_id_2}/set_default"
    )
    assert response.status_code == 200

    response = await authenticated_ac.get("/payments/methods")
    payment_methods = response.json()["payment_methods"]
    assert len(payment_methods) == 2

    is_default1 = payment_methods[0]["is_default"]
    is_default2 = payment_methods[1]["is_default"]

    assert not is_default1
    assert is_default2
