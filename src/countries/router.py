from fastapi import APIRouter

from src.countries.dao import CountryDAO
from src.exceptions import CountryDoesNotExistException


router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/{country_name}")
async def get_country(country_name: str):
    country = await CountryDAO.find_one_or_none(name=country_name)

    if not country:
        raise CountryDoesNotExistException

    return country


# @router.post("/")
# async def add_country(country: CountryCreate) -> Optional[Country]:
#     # Check superuser
#     country = await CountryDAO.add(country_name)
#
#     if not country:
#         raise Exception
#     return country
