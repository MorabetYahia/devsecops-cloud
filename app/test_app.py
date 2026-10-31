import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def test_index_renvoie_le_message(client):
    r = client.get("/")
    assert r.status_code == 200
    data = r.get_json()
    assert data["message"] == "Hello DevSecOps"
    assert "version" in data
    assert "pod" in data


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_metrics_exposees(client):
    client.get("/")
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"flask_http_request_total" in r.data


def test_route_inconnue_404(client):
    assert client.get("/nexiste-pas").status_code == 404
