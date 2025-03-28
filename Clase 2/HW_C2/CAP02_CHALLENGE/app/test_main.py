import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_item():
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42}

def test_create_item():
    item_data = {"name": "Test Item", "price": 10.5}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json()["name"] == item_data["name"]
    assert response.json()["price"] == item_data["price"]
    assert "item_id" in response.json()

def test_update_item():
    item_data = {"name": "Updated Item", "price": 20.5}
    response = client.put("/items/42", json=item_data)
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "name": "Updated Item", "price": 20.5}
