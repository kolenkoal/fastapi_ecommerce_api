import pytest
from httpx import AsyncClient


@pytest.fixture
async def authenticated_ac_with_countries(authenticated_ac):
    response = await authenticated_ac.get("/countries")
    assert response.status_code == 200
    return authenticated_ac, response.json()[0]["id"]


@pytest.mark.asyncio
async def test_create_address_not_authenticated(ac):
    address_data = {
        "unit_number": "3A",
        "street_number": "54",
        "address_line1": "Clements Rd",
        "address_line2": "North Shore",
        "city": "Boston",
        "region": "MA",
        "postal_code": "12313",
        "country_id": "1234",
    }

    response = await ac.post(
        "/addresses",
        json=address_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "unit_number,street_number,address_line1,address_line2,city,region,postal_code,status_code",
    [
        ("", "", "", "", "", "", "", 422),
        (
            "!",
            "54",
            "Clements Rd",
            "North Shore",
            "Boston",
            "MA",
            "123134",
            422,
        ),
        (
            "3A",
            "hello",
            "Clements Rd",
            "North Shore",
            "Boston",
            "MA",
            "123134",
            422,
        ),
        ("3A", "54", "47", "24", "Boston", "MA", "123134", 422),
        ("3A", "54", "Clements Rd", "North Shore", "123", "MA", "123134", 422),
        (
            "3A",
            "54",
            "Clements Rd",
            "North Shore",
            "Boston",
            "123",
            "123134",
            422,
        ),
        (
            "3A",
            "54",
            "Clements Rd",
            "North Shore",
            "Boston",
            "123",
            "!_!",
            422,
        ),
    ],
)
async def test_create_address_with_bad_entities(
    authenticated_ac_with_countries,
    authenticated_ac,
    unit_number,
    street_number,
    address_line1,
    address_line2,
    city,
    region,
    postal_code,
    status_code,
):
    authenticated_ac, country_id = authenticated_ac_with_countries
    address_data = {
        "unit_number": unit_number,
        "street_number": street_number,
        "address_line1": address_line1,
        "address_line2": address_line2,
        "city": city,
        "region": region,
        "postal_code": postal_code,
        "country_id": country_id,
    }

    response = await authenticated_ac.post(
        "/addresses",
        json=address_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_create_address(
    authenticated_ac_with_countries, authenticated_ac
):
    authenticated_ac, country_id = authenticated_ac_with_countries
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

    response = await authenticated_ac.post(
        "/addresses",
        json=address_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200

    response = await authenticated_ac.post(
        "/addresses",
        json=address_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_user_addresses(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/addresses")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_address(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/addresses")
    assert response.status_code == 200

    address_id = response.json()["addresses"][0]["id"]
    response = await authenticated_ac.get(f"/addresses/{address_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_user_address(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/addresses")
    assert response.status_code == 200

    address_id = response.json()["addresses"][0]["id"]
    response = await authenticated_ac.get(f"/addresses/{address_id}")
    assert response.status_code == 200

    address_data = {"city": "New City", "postal_code": "11111"}
    response = await authenticated_ac.patch(
        f"/addresses/{address_id}", json=address_data
    )
    new_address_data = response.json()
    assert response.status_code == 200
    assert new_address_data["city"] == "New City"
    assert new_address_data["postal_code"] == "11111"


@pytest.mark.asyncio
async def test_delete_user_address(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/addresses")
    assert response.status_code == 200

    address_id = response.json()["addresses"][0]["id"]
    response = await authenticated_ac.get(f"/addresses/{address_id}")
    assert response.status_code == 200

    response = await authenticated_ac.delete(f"/addresses/{address_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_create_several_addresses(
    authenticated_ac_with_countries, authenticated_ac
):
    authenticated_ac, country_id = authenticated_ac_with_countries
    address_data_boston = {
        "unit_number": "3A",
        "street_number": "54",
        "address_line1": "Clements Rd",
        "address_line2": "North Shore",
        "city": "Boston",
        "region": "MA",
        "postal_code": "12313",
        "country_id": country_id,
    }
    address_data_moscow = {
        "unit_number": "3A",
        "street_number": "54",
        "address_line1": "Clements Rd",
        "address_line2": "North Shore",
        "city": "Moscow",
        "region": "MA",
        "postal_code": "12313",
        "country_id": country_id,
    }

    response = await authenticated_ac.post(
        "/addresses",
        json=address_data_boston,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200

    response = await authenticated_ac.post(
        "/addresses",
        json=address_data_moscow,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_set_default(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/addresses")
    addresses = response.json()["addresses"]
    assert len(addresses) == 2

    is_default1 = addresses[0]["is_default"]
    address_id_2, is_default2 = addresses[1]["id"], addresses[1]["is_default"]
    assert is_default1
    assert not is_default2

    response = await authenticated_ac.post(
        f"/addresses/{address_id_2}/set_default"
    )
    assert response.status_code == 200

    response = await authenticated_ac.get("/addresses")
    addresses = response.json()["addresses"]
    assert len(addresses) == 2

    is_default1 = addresses[0]["is_default"]
    is_default2 = addresses[1]["is_default"]

    assert not is_default1
    assert is_default2
