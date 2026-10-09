from fastapi.testclient import TestClient
from api import app, get_session
import pytest
from database import engine, SessionLocal

@pytest.fixture
def client():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(
    bind=connection,
    join_transaction_mode="create_savepoint"
    )
    def test_get_session():
        yield session

    app.dependency_overrides[get_session] = test_get_session
    yield TestClient(app)
    session.close()
    transaction.rollback()
    connection.close()
    app.dependency_overrides.pop(get_session, None)

# check connection
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
            "message": "TaskFlow API is running"
        }

def test_get_all_tasks_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []

# get all tasks

def test_get_all_tasks(client):
    client.post(
        "/tasks",
        json={
            "task_id": 8,
            "title": "Learn Python"
        }
    )

    client.post(
        "/tasks",
        json={
            "task_id": 9,
            "title": "Learn Docker"
        }
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 8,
            "title": "Learn Python",
            "completed": False
        },
        {
            "id": 9,
            "title": "Learn Docker",
            "completed": False
        }
    ]

# check already exists
def test_find_task_starts_empty(client):
    response = client.get("/tasks/1")

    assert response.status_code == 404

# create task
def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "task_id": 1,
            "title": "Learn Docker"
        }
    )

    assert response.status_code == 201

    assert response.json() == {
        "id": 1,
        "title": "Learn Docker",
        "completed": False
    }

def test_create_task_invalid_id(client):
    response = client.post(
        "/tasks",
        json={
            "task_id": 0,
            "title": "Learn Docker"
        }
    )

    assert response.status_code == 422

def test_create_task_empty_title(client):
    response = client.post(
        "/tasks",
        json={
            "task_id": 2,
            "title": ""
        }
    )

    assert response.status_code == 422

def test_create_task_duplicate_id(client):
    client.post(
        "/tasks",
        json={
            "task_id": 3,
            "title": "Learn Git"
        }
    )

    response = client.post(
        "/tasks",
        json={
            "task_id": 3,
            "title": "Learn Docker"
        }
    )

    assert response.status_code == 409

# find task
def test_find_task(client):
    client.post(
        "/tasks",
        json={
            "task_id": 4,
            "title": "Learn Kubernetes"
        }
    )

    response = client.get("/tasks/4")

    assert response.status_code == 200
    assert response.json() == {
        "id": 4,
        "title": "Learn Kubernetes",
        "completed": False
    }

def test_find_task_not_found(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }

def test_find_task_invalid_id(client):
    response = client.get("/tasks/hello")

    assert response.status_code == 422

# patch complete

def test_complete_task(client):
    client.post(
        "/tasks",
        json={
            "task_id": 5,
            "title": "Learn Docker"
        }
    )

    response = client.patch("/tasks/5/complete")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Task completed successfully"
    }

def test_complete_task_not_found(client):
    response = client.patch("/tasks/999/complete")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }

# delete task

def test_delete_task(client):
    client.post(
        "/tasks",
        json={
            "task_id": 6,
            "title": "Learn Kubernetes"
        }
    )

    response = client.delete("/tasks/6")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Task deleted successfully"
    }

def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }

# update tasks

def test_update_task(client):
    client.post(
        "/tasks",
        json={
            "task_id": 7,
            "title": "Learn Docker"
        }
    )

    response = client.put(
        "/tasks/7",
        json={
            "title": "Learn Advanced Docker"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 7,
        "title": "Learn Advanced Docker",
        "completed": False
    }

def test_update_task_not_found(client):
    response = client.put(
        "/tasks/999",
        json={
            "title": "Learn Advanced Docker"
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }



