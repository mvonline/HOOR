import json

import pytest

from studio.agents import AgentRuntimeError
from studio.approval import approve_plan, submit_for_approval
from studio.db import StudioStore
from studio.models import TaskStatus
from studio.service import bootstrap_alignment
from studio.tasks import run_ready_tasks, run_task


def test_run_ready_writes_evidence(settings, production_responses):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    assert plan is not None
    submit_for_approval(store, plan)
    approve_plan(store, plan.id)
    done = run_ready_tasks(store, plan.id, limit=1)
    assert len(done) == 1
    assert done[0].status == TaskStatus.DONE
    assert done[0].evidence
    output = settings.repo_root / done[0].evidence[0].reference
    assert output.read_text(encoding="utf-8") == "implemented\n"
    assert done[0].evidence[0].kind == "implementation"
    assert any(e.kind == "peer_review" for e in done[0].evidence)
    assert production_responses.call_count == 2


def test_dependency_blocks_until_parent_done(settings, production_responses):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    assert plan is not None
    submit_for_approval(store, plan)
    approve_plan(store, plan.id)
    tasks = store.list_tasks(plan.id)
    ready = [t for t in tasks if t.status == TaskStatus.READY]
    blocked_or_pending = [t for t in tasks if t.depends_on]
    assert ready
    assert blocked_or_pending
    # Run first ready; some dependents may become ready
    run_task(store, ready[0].id)
    refreshed = {t.id: t for t in store.list_tasks(plan.id)}
    assert refreshed[ready[0].id].status == TaskStatus.DONE


@pytest.mark.parametrize("approval", [False, "false"])
def test_rejected_review_never_completes_task(settings, production_responses, approval):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    submit_for_approval(store, plan)
    approve_plan(store, plan.id)
    task = next(t for t in store.list_tasks(plan.id) if t.status == TaskStatus.READY)
    task.max_retries = 0
    store.save_task(task)
    implementation = json.dumps({
        "summary": "Proposed work",
        "files": [{"path": "game/proposal.txt", "content": "proposal"}],
    })
    rejection = json.dumps({"approved": approval, "issues": ["Acceptance unmet"]})
    production_responses.side_effect = [implementation, rejection, implementation, rejection]

    with pytest.raises(AgentRuntimeError, match="Peer review rejected"):
        run_task(store, task.id)

    failed = store.get_task(task.id)
    assert failed.status == TaskStatus.FAILED
    assert not failed.evidence
    assert not failed.outputs.get("agent_report")
    assert production_responses.call_count == 4
    assert all(
        t.status != TaskStatus.READY
        for t in store.list_tasks(plan.id) if task.id in t.depends_on
    )


def test_review_revision_produces_final_file(settings, production_responses):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    submit_for_approval(store, plan)
    approve_plan(store, plan.id)
    task = next(t for t in store.list_tasks(plan.id) if t.status == TaskStatus.READY)
    production_responses.side_effect = [
        json.dumps({"files": [{"path": "game/output.txt", "content": "draft"}]}),
        json.dumps({"approved": False, "issues": ["Fix the output"]}),
        json.dumps({"files": [{"path": "game/output.txt", "content": "revised"}]}),
        json.dumps({"approved": True, "issues": [], "summary": "Revision accepted"}),
    ]

    result = run_task(store, task.id)

    assert result.status == TaskStatus.DONE
    assert (settings.repo_root / "game/output.txt").read_text() == "revised"
    assert production_responses.call_count == 4
    report = settings.repo_root / result.outputs["agent_report"]
    assert "Revision accepted" in report.read_text(encoding="utf-8")
