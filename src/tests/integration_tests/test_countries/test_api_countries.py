import pytest


@pytest.fixture
async def get_all_countries(ac):
    response = await ac.get("/api/countries")
    assert response.status_code == 200
    countries = response.json()

    return ac, countries


@pytest.mark.asyncio
async def test_get_country(ac, get_all_countries):
    ac, countries = get_all_countries
    country_id = countries[0]["id"]

    response = await ac.get(f"/api/countries/{country_id}")

    assert response.status_code == 200
