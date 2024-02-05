import pytest


# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "unit_number,street_number,address_line1,address_line2,city,region,postal_code,status_code",
#     [
#         (
#                 "3A",
#                 "54",
#                 "Clements Rd",
#                 "North Shore",
#                 "Boston",
#                 "MA",
#                 "12313",
#                 200
#         ),
#     ],
# )
# async def test_create_address(
#         authenticated_ac, unit_number, street_number, address_line1,
#         address_line2, city, region,
#         postal_code, status_code
# ):
#     # Make sure the token is present in the cookies
#     assert "ecommerce_token" in authenticated_ac.cookies
#
#     # Use the authenticated_ac to make a POST request to create an address
#     response = await authenticated_ac.get("/countries")
#     assert response.status_code == 200
#
#     country_id = response.json()[0]["id"]
#
#     response = await authenticated_ac.post(
#         "/addresses",
#         json={
#             "unit_number": unit_number,
#             "street_number": street_number,
#             "address_line1": address_line1,
#             "address_line2": address_line2,
#             "city": city,
#             "region": region,
#             "postal_code": postal_code,
#             "country_id": country_id,
#         },
#         headers={"Content-Type": "application/json"}
#     )
#
#     assert response.status_code == status_code


@pytest.mark.asyncio
async def test_get_address(authenticated_ac):
    print(authenticated_ac.cookies["ecommerce_token"])
    assert "ecommerce_token" in authenticated_ac.cookies

    response = await authenticated_ac.get(
        "/addresses",
    )

    assert response.status_code == 404
