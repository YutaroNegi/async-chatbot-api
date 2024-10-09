import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_access_protected_route_without_token():
    response = client.post("/messages/", json={"message": "Hello"})
    assert response.status_code == 401


def test_access_protected_route_with_invalid_token():
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/messages/", headers=headers, json={"message": "Hello"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
