from services.fastapi.app import app

from fastapi.testclient import TestClient

def test_health_response():

    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()

def test_ping_pong_response():

    client = TestClient(app)
    response = client.get("/health/ping")

    assert response.status_code == 200
