from src.countries.models import Country
from src.dao import BaseDAO


class CountryDAO(BaseDAO):
    model = Country
