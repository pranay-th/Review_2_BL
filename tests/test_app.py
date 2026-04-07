import pytest
import json
from unittest.mock import MagicMock
from models.Task import Task
from models.APIClient import TaskManager
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def manager():
    mock_fh = MagicMock()
    mock_fh.read_json.return_value = []
    tm = TaskManager(mock_fh)
    tm.load_tasks()
    return tm


def test_task_to_dict():
    t = Task(1, "Buy milk", "High")
    assert t.to_dict() == {"id": 1, "title": "Buy milk", "priority": "High", "status": "Pending"}


def test_task_from_dict():
    t = Task.from_dict({"id": 2, "title": "Walk dog", "priority": "Low", "status": "Pending"})
    assert t.id == 2
    assert t.title == "Walk dog"


def test_add_and_get_task(manager):
    manager.add_task("Test task", "High")
    tasks = manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test task"


def test_update_task(manager):
    manager.add_task("Old title")
    updated = manager.update_task(1, {"status": "Completed"})
    assert updated["status"] == "Completed"


def test_delete_task(manager):
    manager.add_task("To delete")
    result = manager.delete_task(1)
    assert result is True
    assert manager.get_task_by_id(1) is None


def test_post_task(client):
    res = client.post("/tasks", json={"title": "New task", "priority": "Medium"})
    assert res.status_code == 201
    assert res.get_json()["title"] == "New task"


def test_get_tasks(client):
    res = client.get("/tasks")
    assert res.status_code == 200


def test_delete_task_endpoint(client):
    client.post("/tasks", json={"title": "Delete me"})
    res = client.delete("/tasks/1")
    assert res.status_code == 200
