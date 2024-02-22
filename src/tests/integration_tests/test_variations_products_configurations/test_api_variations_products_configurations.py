import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product_configuration_not_authenticated(ac):
    product_item_data = {"product_item_id": 1, "variation_option_id": 1}

    response = await ac.post(
        "/products/configurations",
        json=product_item_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    "price,quantity_in_stock,status_code",
    [
        ("1.99", 4, 200),
    ],
)
@pytest.mark.asyncio
async def test_create_product_item(
    admin_ac, price, quantity_in_stock, status_code, temp_product_items_file
):
    response = await admin_ac.get("/products")
    assert response.status_code == 200

    product_id = response.json()["products"][0]["id"]

    form_data = {
        "price": price,
        "quantity_in_stock": quantity_in_stock,
        "product_id": product_id,
    }

    with open(temp_product_items_file, "rb") as file:
        files = {"file": file}
        response = await admin_ac.post(
            "/products/items", files=files, data=form_data
        )
        assert response.status_code == status_code


@pytest.mark.asyncio
async def test_create_product_configuration(admin_ac):
    response = await admin_ac.get("/products/items")
    assert response.status_code == 200

    product_item_id = response.json()["product_items"][0]["id"]

    response = await admin_ac.get("/variation_options")
    assert response.status_code == 200

    variation_option_id = response.json()["variation_options"][0]["id"]

    product_configuration_data = {
        "product_item_id": product_item_id,
        "variation_option_id": variation_option_id,
    }

    response = await admin_ac.post(
        f"/products/configurations?product_item_id={product_item_id}&variation_option_id={variation_option_id}",
        headers={"Accept": "application/json"},
        json=product_configuration_data,
    )

    assert response.status_code == 200


#
@pytest.mark.asyncio
async def test_get_product_items(ac: AsyncClient):
    response = await ac.get("/products/configurations")

    assert response.status_code == 200

    product_items = response.json()["product_configurations"]

    assert len(product_items) == 1


@pytest.mark.asyncio
async def test_delete_product_item(admin_ac: AsyncClient):
    response = await admin_ac.get("/products/configurations")
    assert response.status_code == 200
    assert len(response.json()["product_configurations"]) == 1

    product_item_id = response.json()["product_configurations"][0][
        "product_item_id"
    ]
    variation_option_id = response.json()["product_configurations"][0][
        "variation_option_id"
    ]

    response = await admin_ac.delete(
        f"/products/configurations?product_item_id={product_item_id}&variation_option_id={variation_option_id}",
    )

    assert response.status_code == 204

    response = await admin_ac.get("/products/configurations")
    assert response.status_code == 404
