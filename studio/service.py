"""High-level studio workflows."""

from __future__ import annotations

from studio.analysis import build_analysis, write_analysis
from studio.approval import approve_plan, reject_plan, submit_for_approval
from studio.config import Settings, ensure_project_dirs, get_settings
from studio.db import StudioStore
from studio.ingestion import ingest_game_story, write_index
from studio.models import (
    Phase,
    PlanDeliverable,
    PlanStatus,
    ProductionPlan,
    StudioStatus,
    utc_now,
)
from studio.planning import build_production_plan, write_plan
from studio.tasks import create_tasks_if_approved, run_ready_tasks, task_counts


def bootstrap_alignment(settings: Settings | None = None) -> dict:
    """Phase A pipeline: ingest → analyze → plan (draft) → persist artifacts."""
    settings = ensure_project_dirs(settings)
    store = StudioStore(settings)

    index = ingest_game_story(settings)
    index_path = write_index(index, settings)

    analysis, analysis_path = write_analysis(build_analysis(index, settings), settings)

    # Supersede previous latest plan so a finer replan can be re-approved cleanly.
    previous = store.latest_plan()
    if previous is not None and previous.status != PlanStatus.SUPERSEDED:
        previous.status = PlanStatus.SUPERSEDED
        previous.updated_at = utc_now()
        store.save_plan(previous)

    plan = build_production_plan(analysis, settings)
    plan_path = write_plan(plan, settings)
    store.save_plan(plan)

    open_decision = settings.decisions_dir / "OPEN-bahram-resources.md"
    if not open_decision.exists():
        open_decision.write_text(
            (
                "# Open decision — Bahram 20-year resource balance\n\n"
                "Status: **OPEN** (requires human)\n\n"
                "Validation report notes that water/food/energy sufficiency for "
                "Bahram's dilated stay is not proven. Do not build slice gameplay "
                "that depends on a resolved answer until this decision is closed.\n"
            ),
            encoding="utf-8",
        )

    store.log_event(
        "alignment_bootstrap",
        {
            "documents": len(index.documents),
            "analysis": str(analysis_path),
            "plan_id": plan.id,
        },
    )
    return {
        "index_path": str(index_path),
        "analysis_path": str(analysis_path),
        "plan_id": plan.id,
        "plan_path": str(plan_path),
        "document_count": len(index.documents),
        "missing_story": index.missing,
    }


def get_status(settings: Settings | None = None) -> StudioStatus:
    settings = ensure_project_dirs(settings)
    store = StudioStore(settings)
    index = ingest_game_story(settings)
    plan = store.latest_plan()
    tasks = store.list_tasks(plan.id) if plan else []

    phase = Phase.A_ALIGNMENT
    analysis_path = settings.analysis_dir / "story-analysis.md"
    if plan and plan.status == PlanStatus.APPROVED:
        phase = Phase.C_PRODUCTION
    elif (settings.repo_root / "studio").exists() and analysis_path.exists():
        # Studio code present + analysis done ⇒ at least Phase B tooling available
        phase = Phase.B_STUDIO
        if plan and plan.status in {PlanStatus.PENDING_APPROVAL, PlanStatus.APPROVED}:
            phase = (
                Phase.C_PRODUCTION
                if plan.status == PlanStatus.APPROVED
                else Phase.B_STUDIO
            )

    return StudioStatus(
        project_id=settings.project_id,
        phase=phase,
        game_story_present=not index.missing,
        document_count=len(index.documents),
        plan_id=plan.id if plan else None,
        plan_status=plan.status if plan else None,
        task_counts=task_counts(tasks),
        analysis_path=(
            str(analysis_path.relative_to(settings.repo_root))
            if analysis_path.exists()
            else None
        ),
        plan_path=plan.markdown_path if plan else None,
    )


def submit_latest(store: StudioStore | None = None) -> dict:
    store = store or StudioStore(get_settings())
    plan = store.latest_plan()
    if plan is None:
        raise RuntimeError("No plan found. Run bootstrap/align first.")

    # Idempotent: already past draft — don't crash the CLI/UI.
    if plan.status == PlanStatus.PENDING_APPROVAL:
        return {
            "plan_id": plan.id,
            "status": plan.status.value,
            "unchanged": True,
            "message": "Plan is already awaiting approval. Run: python -m studio.cli approve",
        }
    if plan.status == PlanStatus.APPROVED:
        return {
            "plan_id": plan.id,
            "status": plan.status.value,
            "unchanged": True,
            "message": (
                "Plan is already approved; submit is not needed. "
                "Next: python -m studio.cli tasks  |  python -m studio.cli run -l 3  "
                "| or start C0 playtest build. "
                "To revise the plan: python -m studio.cli align (creates a new draft)."
            ),
        }
    if plan.status == PlanStatus.SUPERSEDED:
        raise RuntimeError(
            "Latest plan is superseded. Run: python -m studio.cli align"
        )

    plan = submit_for_approval(store, plan)
    return {
        "plan_id": plan.id,
        "status": plan.status.value,
        "unchanged": False,
        "message": "Submitted for approval. Run: python -m studio.cli approve",
    }


def approve_latest(note: str = "Approved by human", store: StudioStore | None = None) -> dict:
    store = store or StudioStore(get_settings())
    plan = store.latest_plan()
    if plan is None:
        raise RuntimeError("No plan found.")
    if plan.status == PlanStatus.APPROVED:
        tasks = store.list_tasks(plan.id)
        return {
            "plan_id": plan.id,
            "status": plan.status.value,
            "unchanged": True,
            "tasks_created": len(tasks),
            "task_counts": task_counts(tasks),
            "message": (
                "Plan already approved. Next: python -m studio.cli run -l 3 "
                "or start implementing C0 (echo playtest)."
            ),
        }
    plan = approve_plan(store, plan.id, note=note, create_tasks=True)
    tasks = store.list_tasks(plan.id)
    return {
        "plan_id": plan.id,
        "status": plan.status.value,
        "unchanged": False,
        "tasks_created": len(tasks),
        "task_counts": task_counts(tasks),
        "message": "Approved and production tasks created.",
    }


def reject_latest(note: str = "Rejected by human", store: StudioStore | None = None) -> dict:
    store = store or StudioStore(get_settings())
    plan = store.latest_plan()
    if plan is None:
        raise RuntimeError("No plan found.")
    plan = reject_plan(store, plan.id, note=note)
    return {"plan_id": plan.id, "status": plan.status.value}


def run_batch(limit: int = 5, store: StudioStore | None = None) -> dict:
    store = store or StudioStore(get_settings())
    plan = store.latest_plan()
    if plan is None:
        raise RuntimeError("No plan found.")
    if plan.status != PlanStatus.APPROVED:
        raise RuntimeError("Plan is not approved; refusing to run production tasks.")
    done = run_ready_tasks(store, plan.id, limit=limit)
    tasks = store.list_tasks(plan.id)
    return {
        "ran": [t.id for t in done],
        "task_counts": task_counts(tasks),
    }


def save_plan_edits(
    plan: ProductionPlan,
    *,
    summary: str,
    phases: list[str],
    risks: list[str],
    human_gates: list[str],
    deliverables: list[PlanDeliverable] | list[dict],
    store: StudioStore | None = None,
    reset_to_draft: bool = True,
) -> dict:
    """Persist UI/CLI edits. Editing an approved plan resets it to draft (re-approval required)."""
    store = store or StudioStore(get_settings())
    existing = store.get_plan(plan.id)
    if existing is None:
        raise RuntimeError(f"Plan not found: {plan.id}")

    parsed: list[PlanDeliverable] = []
    for item in deliverables:
        if isinstance(item, PlanDeliverable):
            parsed.append(item)
        else:
            deps = item.get("depends_on", [])
            if isinstance(deps, str):
                deps = [d.strip() for d in deps.split(",") if d.strip()]
            parsed.append(
                PlanDeliverable(
                    id=str(item.get("id", "")).strip(),
                    title=str(item.get("title", "")).strip(),
                    layer=str(item.get("layer", "")).strip(),
                    acceptance=str(item.get("acceptance", "")).strip(),
                    agent_role=str(item.get("agent_role", item.get("role", ""))).strip(),
                    depends_on=list(deps),
                )
            )
    if not parsed:
        raise RuntimeError("Plan must keep at least one deliverable.")
    if any(not d.id or not d.title for d in parsed):
        raise RuntimeError("Each deliverable needs a non-empty id and title.")

    was_approved = existing.status == PlanStatus.APPROVED
    existing.summary = summary.strip()
    existing.phases = [p.strip() for p in phases if p.strip()]
    existing.risks = [r.strip() for r in risks if r.strip()]
    existing.human_gates = [g.strip() for g in human_gates if g.strip()]
    existing.deliverables = parsed
    existing.updated_at = utc_now()

    if reset_to_draft and existing.status in {
        PlanStatus.APPROVED,
        PlanStatus.PENDING_APPROVAL,
        PlanStatus.REJECTED,
    }:
        existing.status = PlanStatus.DRAFT
        existing.approval_note = None
        existing.approved_at = None

    write_plan(existing, store.settings)
    store.save_plan(existing)
    store.log_event(
        "plan_edited",
        {
            "plan_id": existing.id,
            "status": existing.status.value,
            "was_approved": was_approved,
            "deliverable_count": len(parsed),
        },
    )
    return {
        "plan_id": existing.id,
        "status": existing.status.value,
        "deliverable_count": len(parsed),
        "reapproval_required": was_approved or existing.status == PlanStatus.DRAFT,
        "message": (
            "Saved. Plan reset to draft — submit and approve again."
            if was_approved
            else f"Saved as {existing.status.value}."
        ),
    }


# Re-export helpers used by API/CLI
__all__ = [
    "bootstrap_alignment",
    "get_status",
    "submit_latest",
    "approve_latest",
    "reject_latest",
    "run_batch",
    "save_plan_edits",
    "StudioStore",
    "create_tasks_if_approved",
]
