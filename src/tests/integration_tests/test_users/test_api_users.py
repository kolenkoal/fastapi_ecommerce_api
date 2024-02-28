import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email,first_name,last_name,password,status_code",
    [
        ("test@test.com", "test", "test", "test1", 201),
        ("hello@test.com", "Hi", "hi", "yoooo!", 201),
        ("test@test.com", "test", "test", "test1", 400),
        ("test1@test.com", "t", "test", "test1", 422),
        ("test1@test.com", "to", "t", "test1", 422),
        ("test1@test.com", "to", "t", "1", 422),
    ],
)
async def test_register_user(
    email, first_name, last_name, password, status_code, ac: AsyncClient
):
    response = await ac.post(
        "api/auth/register",
        json={
            "email": email,
            "last_name": last_name,
            "first_name": first_name,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username,password,status_code",
    [
        ("test@test.com", "test1", 204),
        ("hello@test.com", "yoooo!", 204),
        ("test@test.com", "test2", 400),
        ("test@test.com", "yoooo", 400),
    ],
)
async def test_login_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "api/auth/login",
        data={
            "username": username,
            "password": password,
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    assert response.status_code == status_code
