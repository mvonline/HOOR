import json
from unittest.mock import Mock

from fastapi.testclient import TestClient

from studio.api import app


def test_api_align_status_approve_flow(settings, monkeypatch):
    monkeypatch.setenv("STUDIO_REPO_ROOT", str(settings.repo_root))
    monkeypatch.setenv("STUDIO_PROJECT_ID", settings.project_id)
    # Exercise production and peer review without calling a live AI provider.
    agent_request = Mock(side_effect=[
        json.dumps({
            "summary": "Created the test deliverable",
            "files": [{"path": "game/test-deliverable.txt", "content": "API test output\n"}],
            "acceptance_evidence": ["Test deliverable written"],
            "assumptions": [],
        }),
        json.dumps({"approved": True, "issues": [], "summary": "Test review passed"}),
    ])
    monkeypatch.setattr("studio.agents._request", agent_request)

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
    assert run.status_code == 200, run.text
    assert run.json()["ran"]
    assert run.json()["produced_files"] == ["game/test-deliverable.txt"]
    assert (settings.repo_root / "game/test-deliverable.txt").read_text(
        encoding="utf-8"
    ) == "API test output\n"
    assert agent_request.call_count == 2
    completed = [task for task in client.get("/tasks").json() if task["id"] in run.json()["ran"]]
    assert len(completed) == 1
    assert completed[0]["status"] == "done"
    assert any(item["kind"] == "peer_review" for item in completed[0]["evidence"])
