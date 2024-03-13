import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_variation_option(ac):
    variation_option_data = {"value": "Hello", "variation_id": 1}

    response = await ac.post(
        "/api/variations/options",
        json=variation_option_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value,variation_id,status_code",
    [
        ("", 1, 422),
        ("Color", "00c73462-a4d9-472c-98fb-119d67fa587d", 404),
    ],
)
async def test_create_variation_options_with_bad_entities(
    admin_ac, value, variation_id, status_code
):
    variation_option_data = {
        "value": value,
        "variation_id": variation_id,
    }

    response = await admin_ac.post(
        "/api/variations/options",
        json=variation_option_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,category_id,status_code",
    [
        ("LOKKK", 3, 200),
    ],
)
async def test_create_variations(admin_ac, name, category_id, status_code):
    variation_data = {"name": name, "category_id": category_id}

    response = await admin_ac.post(
        "/api/variations",
        json=variation_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value,status_code",
    [
        ("XS", 200),
        ("XS", 422),
    ],
)
async def test_create_variation_options(admin_ac, value, status_code):
    response = await admin_ac.get("/api/variations")
    assert response.status_code == 200

    variation_id = response.json()["variations"][0]["id"]

    variation_option_data = {"value": value, "variation_id": variation_id}

    response = await admin_ac.post(
        "/api/variations/options",
        json=variation_option_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_get_variation_options(ac: AsyncClient):
    response = await ac.get("/api/variations/options")
    assert response.status_code == 200

    variations = response.json()["variation_options"]

    assert len(variations) == 2
    assert variations[0]["value"] == "XS"


@pytest.mark.asyncio
async def test_get_variation_option(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/api/variations/options")
    assert response.status_code == 200

    variation_option_id = response.json()["variation_options"][0]["id"]

    response = await authenticated_ac.get(
        f"/api/variations/options/{variation_option_id}"
    )
    assert response.status_code == 200


#


@pytest.mark.asyncio
async def test_change_variation_option(admin_ac: AsyncClient):
    response = await admin_ac.get("/api/variations/options")
    assert response.status_code == 200

    variation_option_id = response.json()["variation_options"][0]["id"]

    new_variation_option_data = {
        "value": "S",
    }
    response = await admin_ac.patch(
        f"/api/variations/options/{variation_option_id}",
        json=new_variation_option_data,
    )

    assert response.status_code == 200

    assert response.json()["value"] == "S"


@pytest.mark.asyncio
async def test_delete_variation_option(admin_ac: AsyncClient):
    response = await admin_ac.get("/api/variations/options")
    assert response.status_code == 200

    variation_option_id = response.json()["variation_options"][0]["id"]

    response = await admin_ac.delete(
        f"/api/variations/options/{variation_option_id}",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/api/variations/options")
    assert response.status_code == 200
    assert len(response.json()) == 1
