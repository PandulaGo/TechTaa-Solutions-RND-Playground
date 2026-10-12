import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def fresh_database():
    """Run before every test: start with empty tables."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_health():
    response = client.get("/health")
    
    assert response.status_code == 200

def test_create_and_list_tasks():
    created = client.post("/tasks", json={"title": "Test Task"})
    
    assert created.status_code == 201
    assert created.json()["title"] == "Test Task"
    assert created.json()["done"] is False

    listed = client.get("/tasks")
    
    assert len(listed.json()) == 1

def test_update_task():
    task_id = client.post("/tasks", json={"title": "Update Test"}).json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"done": True})

    assert response.status_code == 200
    assert response.json()["done"] is True
    assert response.json()["title"] == "Update Test"

def test_delete_task():
    task_id = client.post("/tasks", json={"title": "Delete Test"}).json()["id"]
    
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get("/tasks").json() == []

def test_missing_task_returns_404():
    assert client.delete("/tasks/999").status_code == 404

def test_empty_title_is_rejected():
    response = client.post("/tasks", json={"title": ""})
    
    assert response.status_code == 422