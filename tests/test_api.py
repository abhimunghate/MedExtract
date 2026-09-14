import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"


def test_extract_endpoint(client):
    response = client.post(
        "/api/extract",
        json={
            "text": "The patient has fever and takes Paracetamol."
        }
    )

    assert response.status_code == 200

    data = response.get_json()
    
    assert "entities" in data

    assert "entity_count" in data

    assert data["status"] == "success"
    assert data["entity_count"] >= 1


def test_extract_without_text(client):
    response = client.post(
        "/api/extract",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"


def test_extract_with_empty_text(client):
    response = client.post(
        "/api/extract",
        json={
            "text": ""
        }
    )

    assert response.status_code == 400