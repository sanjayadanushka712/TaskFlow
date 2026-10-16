from fastapi.testclient import TestClient
from api import app, get_session
import pytest
from database import engine, SessionLocal
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import select, func
from models import IdempotencyRecord, Task
import threading
from app import Taskflow

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
    
def test_create_task_is_idempotent(client):
    created = client.post(
        "/tasks",
        json={
            "task_id": 1,
            "title": "Learn Docker"
        }
    )
    assert created.status_code == 201
    second = client.post(
        "/tasks",
        json={
            "task_id": 1,
            "title": "Learn Docker"
        }
    )
    assert second.status_code == 409
    result = client.get("/tasks/1")
    assert result.status_code == 200
    assert result.json() == {
            "id": 1,
            "title": "Learn Docker",
            "completed": False
        }  

def test_create_task_retry_returns_original_result(client):
    payload = {
        "task_id": 100,
        "title": "Learn Docker"
    }
    headers = {
        "Idempotency-Key": "task-create-001"
    }

    first = client.post(
        "/tasks",
        json=payload,
        headers=headers
    )

    second = client.post(
        "/tasks",
        json=payload,
        headers=headers
    )
    
    assert first.status_code == 201
    assert second.status_code == 201

    assert first.json()["id"] == second.json()["id"]
    assert first.json()["title"] == second.json()["title"]

    result = client.get("/tasks/100")
    assert result.status_code == 200
    assert result.json()["title"] == "Learn Docker"

def test_create_task_retry_with_different_payload_returns_409(client):
    payload1 = {
        "task_id": 100,
        "title": "Learn Docker"
    }
    payload2 = {
            "task_id": 100,
            "title": "Learn Python"
        }
    headers = {
        "Idempotency-Key": "task-create-001"
    }

    first = client.post(
        "/tasks",
        json=payload1,
        headers=headers
    )

    second = client.post(
        "/tasks",
        json=payload2,
        headers=headers
    )
    
    assert first.status_code == 201
    assert second.status_code == 409

    result = client.get("/tasks/100")
    assert result.status_code == 200
    assert result.json()["title"] == "Learn Docker"

def test_create_task_handles_integrity_error(client):
    with patch(
        "api.Taskflow.create_task",
        side_effect=IntegrityError("INSERT", {}, Exception("duplicate"))
    ):
        response = client.post(
            "/tasks",
            json={"task_id": 999, "title": "Learn Python"}
        )

    assert response.status_code == 409
    assert response.json()["detail"] == "Task ID conflicts with existing data"

def test_create_task_with_whitespace_title(client):
    response = client.post(
        "/tasks",
        json={"task_id": 999, "title": "   "}
    )

    assert response.status_code == 422
    assert 'detail' in response.json()
    result = client.get("/tasks/999")
    assert result.status_code == 404

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


def test_concurrent_idempotent_task_creation():
    task_id = 9001
    key = "concurrent-test-9001"
    payload = {
    "task_id": task_id,
    "title": "Test concurrent creation",
    }

    headers = {"Idempotency-Key": key}
    # Remove only this test's old data, if a previous run left any.
    with SessionLocal() as cleanup_session:
        cleanup_session.query(IdempotencyRecord).filter_by(key=key).delete()
        cleanup_session.query(Task).filter_by(id=task_id).delete()
        cleanup_session.commit()

    try:
        # Force both requests to reach task creation before either proceeds.
        barrier = threading.Barrier(2)
        original_create_task = Taskflow.create_task

        def synchronized_create_task(self, task_id, title):
            barrier.wait(timeout=10)
            return original_create_task(self, task_id, title)

        with patch.object(
            Taskflow,
            "create_task",
            synchronized_create_task,
        ):
            def send_request():
                # Each request gets its own HTTP client and database session.
                with TestClient(app) as client:
                    return client.post(
                        "/tasks",
                        json=payload,
                        headers=headers,
                    )

            with ThreadPoolExecutor(max_workers=2) as executor:
                future_a = executor.submit(send_request)
                future_b = executor.submit(send_request)

                response_a = future_a.result()
                response_b = future_b.result()

        # Both requests should return the same successful result.
        assert response_a.status_code == 201
        assert response_b.status_code == 201
        assert response_a.json() == response_b.json()

        # Verify persisted state using a fresh database session.
        with SessionLocal() as verify_session:
            task_count = (
                verify_session.query(Task)
                .filter_by(id=task_id)
                .count()
            )
            record_count = (
                verify_session.query(IdempotencyRecord)
                .filter_by(key=key)
                .count()
            )

        assert task_count == 1
        assert record_count == 1

    finally:
        # Clean up even if an assertion or request fails.
        with SessionLocal() as cleanup_session:
            cleanup_session.query(IdempotencyRecord).filter_by(key=key).delete()
            cleanup_session.query(Task).filter_by(id=task_id).delete()
            cleanup_session.commit()


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
     
def test_complete_task_is_idempotent(client):
    created =client.post(
        "/tasks",
        json={
            "task_id": 5,
            "title": "Learn Docker"
        }
    )
    assert created.status_code == 201
    first = client.patch("/tasks/5/complete")
    second = client.patch("/tasks/5/complete")

    assert first.status_code == 200
    assert second.status_code == 200
    result = client.get("/tasks/5")
    assert result.json()["completed"] is True
    assert result.json()["title"] == "Learn Docker"
    assert result.status_code == 200

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
    
def test_delete_task_is_idempotent(client):
    created = client.post(
        "/tasks",
        json={
            "task_id": 6,
            "title": "Learn Kubernetes"
        }
    )
    assert created.status_code == 201
    first = client.delete("/tasks/6")
    second = client.delete("/tasks/6")
    
    assert first.status_code == 200
    assert second.status_code == 404
    result = client.get("/tasks/6")
    assert result.status_code == 404
    assert result.json()["detail"] == "Task not found"
    
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
    
def test_update_task_with_whitespace_title(client):
    client.post(
        "/tasks",
        json={"task_id": 998, "title": "Original title"}
    )

    response = client.put(
        "/tasks/998",
        json={"title": "   "}
    )

    assert response.status_code == 422

    result = client.get("/tasks/998")
    assert result.status_code == 200
    assert result.json()["title"] == "Original title"

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




