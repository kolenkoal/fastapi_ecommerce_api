import json
import os
import sys

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from src.countries.models import Country
from src.users.models import Role, User


sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from src.config import settings  # noqa
from src.database import Base, async_engine, async_session_factory  # noqa
from src.main import app as fastapi_app  # noqa


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"src/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    try:
        users = open_mock_json("users")
        roles = open_mock_json("roles")
        countries = open_mock_json("countries")

        async with async_session_factory() as session:
            add_roles = insert(Role).values(roles)

            print("Hello")

            await session.execute(add_roles)

            await session.commit()

        async with async_session_factory() as session:
            add_users = insert(User).values(users)
            add_countries = insert(Country).values(countries)

            await session.execute(add_users)
            await session.execute(add_countries)

            await session.commit()
    except Exception as e:
        print(f"An error occurred during database setup: {e}")


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "test@test.com",
                "password": "test",
            },
        )
        assert ac.cookies["booking_access_token"]
        yield ac
