"""Integration tests for LinkSnap API.

Uses FastAPI TestClient — no Azure dependencies required for unit tests.
"""

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_link_returns_201():
    response = client.post(
        "/links",
        json={
            "destination_url": "https://example.com",
            "tenant_id": "test-tenant",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert "short_code" in body
    assert len(body["short_code"]) == 7
    assert body["destination_url"] == "https://example.com/"
    assert body["click_count"] == 0


def test_create_link_validates_url():
    response = client.post(
        "/links",
        json={"destination_url": "not-a-url"},
    )
    assert response.status_code == 422


def test_resolve_nonexistent_link_returns_404():
    response = client.get("/links/nonexist")
    assert response.status_code == 404
    assert response.json()["error"] == "not_found"
