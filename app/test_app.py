import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def test_page_accueil(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.mimetype == "text/html"
    assert b"Yahia Morabet" in r.data


def test_api_info(client):
    data = client.get("/api/info").get_json()
    assert data["message"] == "Hello DevSecOps"
    assert {"pod", "version", "uptime_seconds"} <= data.keys()


def test_entetes_securite(client):
    r = client.get("/")
    assert "default-src 'none'" in r.headers["Content-Security-Policy"]
    assert r.headers["X-Content-Type-Options"] == "nosniff"


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
