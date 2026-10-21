import pytest

from studio.approval import approve_plan, submit_for_approval
from studio.db import StudioStore
from studio.models import Evidence, TaskStatus
from studio.service import bootstrap_alignment
from studio.tasks import run_task


def test_retry_then_succeed(settings):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    assert plan is not None
    submit_for_approval(store, plan)
    approve_plan(store, plan.id)
    ready = next(t for t in store.list_tasks(plan.id) if t.status == TaskStatus.READY)

    calls = {"n": 0}

    def flaky(task):
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("transient")
        return [Evidence(kind="test", reference=f"ok-{task.id}")]

    result = run_task(store, ready.id, handler=flaky)
    assert result.status == TaskStatus.DONE
    assert result.retries == 2


def test_retry_exhausted_marks_failed(settings):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    assert plan is not None
    submit_for_approval(store, plan)
    approve_plan(store, plan.id)
    ready = next(t for t in store.list_tasks(plan.id) if t.status == TaskStatus.READY)
    ready.max_retries = 1
    store.save_task(ready)

    def always_fail(_task):
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        run_task(store, ready.id, handler=always_fail)

    failed = store.get_task(ready.id)
    assert failed is not None
    assert failed.status == TaskStatus.FAILED
    assert failed.retries > failed.max_retries


def test_state_survives_new_store_instance(settings):
    bootstrap_alignment(settings)
    store1 = StudioStore(settings)
    plan = store1.latest_plan()
    assert plan is not None
    submit_for_approval(store1, plan)
    approve_plan(store1, plan.id)

    store2 = StudioStore(settings)
    plan2 = store2.latest_plan()
    assert plan2 is not None
    assert plan2.id == plan.id
    assert plan2.status.value == "approved"
    assert store2.list_tasks(plan2.id)
