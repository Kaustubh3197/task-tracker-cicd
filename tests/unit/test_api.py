"""API tests: call the HTTP endpoints through Flask's test client (no real server needed)."""


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_home_page_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Task Tracker" in res.data


def test_list_starts_empty(client):
    body = client.get("/api/tasks").get_json()
    assert body["tasks"] == []
    assert body["summary"]["total"] == 0


def test_create_task(client):
    res = client.post("/api/tasks", json={"title": "  Write tests  "})
    assert res.status_code == 201
    assert res.get_json() == {"id": 1, "title": "Write tests", "done": False}


def test_create_task_rejects_empty_title(client):
    res = client.post("/api/tasks", json={"title": ""})
    assert res.status_code == 400
    assert "required" in res.get_json()["error"]


def test_create_task_rejects_missing_body(client):
    res = client.post("/api/tasks", data="not json")
    assert res.status_code == 400


def test_mark_task_done(client):
    client.post("/api/tasks", json={"title": "Ship it"})
    res = client.patch("/api/tasks/1", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True

    summary = client.get("/api/tasks").get_json()["summary"]
    assert summary == {"total": 1, "done": 1, "remaining": 0, "percent_done": 100}


def test_update_rejects_non_boolean(client):
    client.post("/api/tasks", json={"title": "Ship it"})
    res = client.patch("/api/tasks/1", json={"done": "yes"})
    assert res.status_code == 400


def test_delete_task(client):
    client.post("/api/tasks", json={"title": "Temporary"})
    assert client.delete("/api/tasks/1").status_code == 204
    assert client.get("/api/tasks").get_json()["tasks"] == []


def test_missing_task_returns_404(client):
    assert client.patch("/api/tasks/99", json={"done": True}).status_code == 404
    assert client.delete("/api/tasks/99").status_code == 404
