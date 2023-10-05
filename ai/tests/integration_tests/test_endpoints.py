import httpx
from config import URL


def test_heartbeat(base_url=URL):
    url = f"{base_url}/"
    response = httpx.get(url)
    assert response.status_code == 200


def test_predict(headers, base_url=URL):
    url = f"{base_url}/predict"

    response = httpx.post(url, headers=headers)

    assert response.status_code == 200
