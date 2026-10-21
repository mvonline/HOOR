from fastapi.testclient import TestClient

from studio.api import app


def test_api_align_status_approve_flow(settings, monkeypatch):
    monkeypatch.setenv("STUDIO_REPO_ROOT", str(settings.repo_root))
    monkeypatch.setenv("STUDIO_PROJECT_ID", settings.project_id)

    client = TestClient(app)
    assert client.get("/health").json()["ok"] is True

    align = client.post("/align")
    assert align.status_code == 200, align.text
    plan_id = align.json()["plan_id"]

    status = client.get("/status")
    assert status.status_code == 200
    assert status.json()["plan_id"] == plan_id
    assert status.json()["game_story_present"] is True

    submit = client.post("/plans/submit")
    assert submit.status_code == 200
    assert submit.json()["status"] == "pending_approval"

    approve = client.post("/plans/approve", json={"note": "ship it"})
    assert approve.status_code == 200
    assert approve.json()["status"] == "approved"
    assert approve.json()["tasks_created"] > 0

    tasks = client.get("/tasks")
    assert tasks.status_code == 200
    assert len(tasks.json()) > 0

    run = client.post("/tasks/run", json={"limit": 1})
    assert run.status_code == 200
    assert run.json()["ran"]
