import httpx
from config import LOGIN_NAME, LOGIN_PASSWORD, URL
from pytest import fixture


@fixture
def headers(base_url=URL):
    auth_data = {"username": LOGIN_NAME, "password": LOGIN_PASSWORD}

    url = f"{base_url}/auth/jwt/login"
    response = httpx.post(url, data=auth_data)

    assert response.status_code == 200
    assert "access_token" in response.json()

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    return headers
