import pytest


@pytest.mark.asyncio
async def test_get_product_categories(ac):
    response = await ac.get("/countries")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_product_category(ac):
    response = await ac.get("/countries")

    country_id = response.json()[0]["id"]

    response = await ac.get(f"countries/{country_id}")

    assert response.status_code == 200
