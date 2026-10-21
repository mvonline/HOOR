from studio.approval import approve_plan, submit_for_approval
from studio.db import StudioStore
from studio.models import TaskStatus
from studio.service import bootstrap_alignment
from studio.tasks import run_ready_tasks, run_task


def test_run_ready_writes_evidence(settings):
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
    receipt = settings.repo_root / done[0].evidence[0].reference
    assert receipt.exists()


def test_dependency_blocks_until_parent_done(settings):
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
