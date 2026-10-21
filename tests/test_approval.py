import pytest

from studio.approval import approve_plan, reject_plan, submit_for_approval
from studio.db import StudioStore
from studio.models import PlanStatus
from studio.planning import build_production_plan
from studio.service import bootstrap_alignment
from studio.tasks import ApprovalRequiredError, create_tasks_if_approved, run_task


def test_cannot_create_tasks_before_approval(settings):
    store = StudioStore(settings)
    plan = build_production_plan(settings=settings)
    store.save_plan(plan)
    with pytest.raises(ApprovalRequiredError):
        create_tasks_if_approved(store, plan)


def test_approve_creates_tasks(settings):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    assert plan is not None
    submit_for_approval(store, plan)
    approved = approve_plan(store, plan.id, note="ok")
    assert approved.status == PlanStatus.APPROVED
    tasks = store.list_tasks(plan.id)
    assert len(tasks) == len(approved.deliverables)
    assert any(t.status.value == "ready" for t in tasks)


def test_reject_blocks_run(settings):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    assert plan is not None
    reject_plan(store, plan.id, note="no")
    plan = store.get_plan(plan.id)
    assert plan is not None
    assert plan.status == PlanStatus.REJECTED
    with pytest.raises(ApprovalRequiredError):
        create_tasks_if_approved(store, plan)


def test_submit_when_already_approved_is_idempotent(settings):
    from studio import service

    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    assert plan is not None
    submit_for_approval(store, plan)
    approve_plan(store, plan.id)
    result = service.submit_latest(store)
    assert result["status"] == "approved"
    assert result["unchanged"] is True
    assert "already approved" in result["message"].lower()


def test_run_requires_approval(settings):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    assert plan is not None
    # Force-create tasks bypassing gate would be wrong; instead save unapproved and try run
    plan.status = PlanStatus.DRAFT
    store.save_plan(plan)
    # Manually insert a task as if someone cheated
    from studio.models import Task, TaskStatus

    task = Task(
        id="task-cheat",
        plan_id=plan.id,
        title="cheat",
        role="QA",
        status=TaskStatus.READY,
        acceptance="x",
    )
    store.save_task(task)
    with pytest.raises(ApprovalRequiredError):
        run_task(store, task.id)
