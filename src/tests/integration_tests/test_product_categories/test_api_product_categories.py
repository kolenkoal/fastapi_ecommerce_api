import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category_not_authenticated(ac):
    product_category_data = {
        "name": "Trousers",
    }

    response = await ac.post(
        "/products/categories",
        json=product_category_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,parent_category_id,status_code",
    [
        ("", None, 422),
        ("47", None, 422),
        ("Pants", 600, 404),
    ],
)
async def test_create_product_categories_with_bad_entities(
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


@pytest.mark.parametrize(
    "name,parent_category_id,status_code",
    [
        ("Tops", None, 200),
        ("Tops", None, 422),
        ("Blazers", 1, 200),
        ("Pants", 6, 404),
    ],
)
@pytest.mark.asyncio
async def test_create_product_categories(
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
async def test_get_user_product_categories(ac: AsyncClient):
    response = await ac.get("/products/categories")

    assert response.status_code == 200

    product_categories = response.json()["product_categories"]

    assert len(product_categories) == 2
    assert product_categories[0]["name"] == "Tops"


@pytest.mark.asyncio
async def test_get_product_category(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/products/categories/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_product_category(admin_ac: AsyncClient):
    new_category_data = {
        "name": "Tops",
    }
    response = await admin_ac.patch(
        "/products/categories/1",
        json=new_category_data,
    )

    assert response.status_code == 422

    new_category_data = {"name": "Bottoms", "parent_category_id": 2}

    response = await admin_ac.patch(
        "/products/categories/1",
        json=new_category_data,
    )
    assert response.status_code == 200

    assert response.json()["name"] == "Bottoms"
    assert response.json()["parent_category_id"] == 2


@pytest.mark.asyncio
async def test_delete_product_category(admin_ac: AsyncClient):
    response = await admin_ac.get("/products/categories")
    assert len(response.json()["product_categories"]) == 2

    response = await admin_ac.delete(
        "/products/categories/1",
    )
    assert response.status_code == 204

    response = await admin_ac.get("/products/categories")
    assert response.status_code == 404
