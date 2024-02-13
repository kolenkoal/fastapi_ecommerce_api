import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_variation(ac):
    variation_data = {"name": "Hello", "category_id": 1}

    response = await ac.post(
        "/variations",
        json=variation_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,category_id,status_code",
    [
        ("", 1, 422),
        ("47", 1, 422),
        ("Color", 600, 404),
    ],
)
async def test_create_variations_with_bad_entities(
    admin_ac, name, category_id, status_code
):
    variation_data = {
        "name": name,
        "category_id": category_id,
    }

    response = await admin_ac.post(
        "/variations",
        json=variation_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "name,parent_category_id,status_code",
    [
        ("Tops", None, 200),
        ("T-shirts", 3, 200),
    ],
)
@pytest.mark.asyncio
async def test_create_product_category(
    admin_ac, name, parent_category_id, status_code
):
    product_category_data = {
        "name": name,
        "parent_category_id": parent_category_id,
    }
    response = await admin_ac.post(
        "/products/categories",
        json=product_category_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,category_id,status_code",
    [
        ("Color", 3, 200),
        ("Color", 3, 422),
        ("Love", 4, 200),
        ("Size", 900, 404),
    ],
)
async def test_create_variations(admin_ac, name, category_id, status_code):
    variation_data = {"name": name, "category_id": category_id}

    response = await admin_ac.post(
        "/variations",
        json=variation_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_get_variations(ac: AsyncClient):
    response = await ac.get("/variations")
    assert response.status_code == 200

    variations = response.json()["variations"]

    assert len(variations) == 3
    assert variations[0]["name"] == "Color"


@pytest.mark.asyncio
async def test_get_variation(admin_ac: AsyncClient):
    response = await admin_ac.get("/variations")
    assert len(response.json()) == 1
    assert response.status_code == 200

    variation_id = response.json()["variations"][0]["id"]

    response = await admin_ac.get(f"/variations/{variation_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_variation(admin_ac: AsyncClient):
    response = await admin_ac.get("/variations")
    assert response.status_code == 200

    variation_id = response.json()["variations"][2]["id"]

    new_variation_data = {
        "name": "9",
    }
    response = await admin_ac.patch(
        f"/variations/{variation_id}",
        json=new_variation_data,
    )

    assert response.status_code == 422

    new_variation_data = {"name": "BOTTTOMS"}

    response = await admin_ac.patch(
        f"/variations/{variation_id}",
        json=new_variation_data,
    )
    assert response.status_code == 200

    assert response.json()["name"] == "Botttoms"


@pytest.mark.asyncio
async def test_delete_variation(admin_ac: AsyncClient):
    response = await admin_ac.get("/variations")
    assert len(response.json()["variations"]) == 3

    response = await admin_ac.get("/variations")
    assert response.status_code == 200

    variation_id = response.json()["variations"][0]["id"]

    response = await admin_ac.delete(
        f"/variations/{variation_id}",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/variations")
    assert response.status_code == 200

    variation_id = response.json()["variations"][0]["id"]

    response = await admin_ac.delete(
        f"/variations/{variation_id}",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/variations")

    assert len(response.json()) == 1
