"""Human approval gate for production plans."""

from __future__ import annotations

from pathlib import Path

from studio.config import Settings, ensure_project_dirs
from studio.db import StudioStore
from studio.models import PlanStatus, ProductionPlan, utc_now
from studio.planning import write_plan
from studio.tasks import create_tasks_if_approved


class PlanNotFoundError(KeyError):
    pass


class InvalidPlanStateError(RuntimeError):
    pass


def submit_for_approval(store: StudioStore, plan: ProductionPlan) -> ProductionPlan:
    if plan.status not in {PlanStatus.DRAFT, PlanStatus.REJECTED}:
        raise InvalidPlanStateError(
            f"Cannot submit plan in status {plan.status.value}"
        )
    plan.status = PlanStatus.PENDING_APPROVAL
    plan.updated_at = utc_now()
    write_plan(plan, store.settings)
    return store.save_plan(plan)


def approve_plan(
    store: StudioStore,
    plan_id: str,
    note: str = "Approved by human",
    *,
    create_tasks: bool = True,
) -> ProductionPlan:
    plan = store.get_plan(plan_id)
    if plan is None:
        raise PlanNotFoundError(plan_id)
    if plan.status not in {PlanStatus.PENDING_APPROVAL, PlanStatus.DRAFT}:
        raise InvalidPlanStateError(
            f"Plan {plan_id} cannot be approved from status {plan.status.value}"
        )
    plan.status = PlanStatus.APPROVED
    plan.approval_note = note
    plan.approved_at = utc_now()
    write_plan(plan, store.settings)
    store.save_plan(plan)
    store.record_approval(plan_id, "approved", note)

    decision = _write_decision(store.settings, plan, approved=True, note=note)
    store.log_event("decision_written", {"path": str(decision)})

    if create_tasks:
        create_tasks_if_approved(store, plan)
    return plan


def reject_plan(
    store: StudioStore,
    plan_id: str,
    note: str = "Rejected by human",
) -> ProductionPlan:
    plan = store.get_plan(plan_id)
    if plan is None:
        raise PlanNotFoundError(plan_id)
    plan.status = PlanStatus.REJECTED
    plan.approval_note = note
    plan.approved_at = None
    write_plan(plan, store.settings)
    store.save_plan(plan)
    store.record_approval(plan_id, "rejected", note)
    _write_decision(store.settings, plan, approved=False, note=note)
    return plan


def _write_decision(
    settings: Settings,
    plan: ProductionPlan,
    *,
    approved: bool,
    note: str,
) -> Path:
    settings = ensure_project_dirs(settings)
    stamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    path = settings.decisions_dir / f"{stamp}-{plan.id}-{'approved' if approved else 'rejected'}.md"
    path.write_text(
        (
            f"# Decision — {'Approve' if approved else 'Reject'} production plan\n\n"
            f"- Plan ID: `{plan.id}`\n"
            f"- Project: `{plan.project_id}`\n"
            f"- Decision: **{'approved' if approved else 'rejected'}**\n"
            f"- At (UTC): {utc_now().isoformat()}\n"
            f"- Note: {note}\n"
        ),
        encoding="utf-8",
    )
    return path
