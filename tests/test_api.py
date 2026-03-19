import pytest
from httpx import AsyncClient
from urllib.parse import urlparse

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_create_short_url(client: AsyncClient):
    response = await client.post("/shorten", json={"original_url": "https://google.com"})

    assert response.status_code == 201
    data = response.json()
    assert "short_url" in data

    parsed = urlparse(data["short_url"])
    assert parsed.scheme in {"http", "https"}
    assert parsed.netloc
    assert parsed.path and parsed.path != "/"

    response2 = await client.post("/shorten", json={"original_url": "https://google.com"})
    assert response2.status_code == 201
    assert response2.json()["short_url"] == data["short_url"]


async def test_redirect_and_stats(client: AsyncClient):
    create_response = await client.post("/shorten", json={"original_url": "https://example.com"})
    short_url = create_response.json()["short_url"]
    short_id = short_url.split("/")[-1]

    stats_response_before = await client.get(f"/stats/{short_id}")
    assert stats_response_before.status_code == 200
    assert stats_response_before.json()["clicks"] == 0

    redirect_response = await client.get(f"/{short_id}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://example.com/"

    stats_response_after = await client.get(f"/stats/{short_id}")
    assert stats_response_after.status_code == 200
    assert stats_response_after.json()["clicks"] == 1
