from uuid import UUID

from fastapi import APIRouter, status

from src.countries.dao import CountryDAO
from src.countries.exceptions import (
    CountriesNotFoundException,
    CountryNotFoundException,
)
from src.countries.schemas import SCountry
from src.exceptions import raise_http_exception


router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get(
    "",
    name="Get all countries.",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "United States",
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        },
                        {
                            "name": "Angola",
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                        },
                    ]
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "examples": {
                        "Countries not found.": {
                            "summary": "Countries not found.",
                            "value": {"detail": "Countries not found."},
                        },
                    }
                }
            }
        },
    },
)
async def get_all_countries():
    countries = await CountryDAO.find_all()

    if not countries:
        raise CountriesNotFoundException

    return countries


@router.get(
    "/{country_id}",
    name="Get certain country.",
    response_model=SCountry,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "examples": {
                        "Country not found.": {
                            "summary": "Country not found.",
                            "value": {"detail": "Country not found."},
                        },
                    }
                }
            }
        }
    },
)
async def get_country_by_id(country_id: UUID):
    country = await CountryDAO.find_by_id(country_id)

    if not country:
        raise_http_exception(CountryNotFoundException)

    return country
