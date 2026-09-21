from fastapi.testclient import TestClient

from revenue_lens.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_overview_endpoint_returns_metrics() -> None:
    response = client.get("/analytics/overview")

    assert response.status_code == 200
    assert response.json()["transactions"] > 0

