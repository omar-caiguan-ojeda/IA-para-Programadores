import pytest
from fastapi.testclient import TestClient
from app.main import app  # Corrige la importación

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API"}  # Mensaje real de tu app

def test_create_task():
    task_data = {"title": "Test Task"}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    assert response.json()["title"] == task_data["title"]
    assert response.json()["completed"] == False
    assert "id" in response.json()

def test_get_task():
    # Crear una tarea primero
    create_response = client.post("/tasks/", json={"title": "Task to Get"})
    task_id = create_response.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Task to Get"

def test_update_task():
    # Crear una tarea primero
    create_response = client.post("/tasks/", json={"title": "Original Task"})
    task_id = create_response.json()["id"]
    update_data = {"title": "Updated Task", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["completed"] == True