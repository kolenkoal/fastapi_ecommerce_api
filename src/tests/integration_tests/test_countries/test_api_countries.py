import pytest


@pytest.mark.asyncio
async def test_get_countries(ac):
    response = await ac.get("/api/countries")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_country(ac):
    response = await ac.get("/api/countries")

    country_id = response.json()[0]["id"]

    response = await ac.get(f"/api/countries/{country_id}")

    assert response.status_code == 200
