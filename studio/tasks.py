"""Task breakdown and runner with approval gate and retries."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import Any

from studio.config import Settings, get_settings
from studio.db import StudioStore
from studio.models import (
    Evidence,
    PlanStatus,
    ProductionPlan,
    Task,
    TaskStatus,
    utc_now,
)


class ApprovalRequiredError(RuntimeError):
    pass


class TaskExecutionError(RuntimeError):
    pass


def tasks_from_plan(plan: ProductionPlan, settings: Settings | None = None) -> list[Task]:
    settings = settings or get_settings()
    from studio.config import ensure_project_dirs

    settings = ensure_project_dirs(settings)
    work_order_dir = settings.artifacts_dir / "work-orders" / plan.id
    work_order_dir.mkdir(parents=True, exist_ok=True)
    analysis_path = settings.analysis_dir / "story-analysis.json"
    analysis = None
    if analysis_path.exists():
        try:
            from studio.models import StoryAnalysis

            analysis = StoryAnalysis.model_validate_json(
                analysis_path.read_text(encoding="utf-8")
            )
        except Exception:
            # Work orders can still be made from the approved plan if analysis is stale.
            analysis = None
    tasks: list[Task] = []
    for item in plan.deliverables:
        work_order = work_order_dir / f"{item.id}.md"
        facts = analysis.approved if analysis else []
        assumptions = analysis.assumptions if analysis else []
        relevant_facts = [fact for fact in facts if _relevant(item, fact.text)]
        relevant_assumptions = [a for a in assumptions if _relevant(item, a.text)]
        lines = [
            f"# Work order: {item.title}",
            "",
            f"- Deliverable: `{item.id}`",
            f"- Plan: `{plan.id}` (approved)",
            f"- Role: {item.agent_role}",
            f"- Phase: {item.layer}",
            f"- Depends on: {', '.join(item.depends_on) or 'none'}",
            "",
            "## Goal",
            item.title,
            "",
            "## Acceptance checks",
            item.acceptance,
            "",
            "## Approved constraints",
        ]
        lines.extend(
            f"- `{fact.id}` {fact.text} (source: `{fact.source}`)"
            for fact in relevant_facts
        )
        if not relevant_facts:
            lines.append("- Follow `masterPrompt.md` and the cited current design sources; do not invent story facts.")
        lines.extend(["", "## Assumptions to preserve as assumptions"])
        lines.extend(
            f"- `{assumption.id}` {assumption.text} (source: `{assumption.source or 'studio'}`)"
            for assumption in relevant_assumptions
        )
        if not relevant_assumptions:
            lines.append("- Do not convert an unstated guess into approved design.")
        lines.extend(["", "## Source documents"])
        lines.extend(f"- `{source}`" for source in (analysis.source_paths if analysis else []))
        lines.extend(
            [
                "",
                "## Agent instructions",
                "1. Inspect the current repository state before editing.",
                "2. Make the smallest change that satisfies the goal and acceptance checks.",
                "3. Keep source design files in `gameStory/` read-only.",
                "4. Report changed files, evidence, unresolved questions, and any assumptions.",
                "5. Do not claim this work is complete until each acceptance check has evidence.",
                "",
            ]
        )
        work_order.write_text("\n".join(lines), encoding="utf-8")
        tasks.append(
            Task(
                id=f"task-{item.id.lower()}-{uuid.uuid4().hex[:6]}",
                plan_id=plan.id,
                title=item.title,
                role=item.agent_role,
                status=TaskStatus.PENDING,
                inputs={
                    "deliverable_id": item.id,
                    "layer": item.layer,
                    "work_order": str(work_order.relative_to(settings.repo_root)),
                    "source_documents": analysis.source_paths if analysis else [],
                },
                constraints=[
                    "Do not invent story details",
                    "Do not mark done without evidence",
                    "Stay inside approved plan scope",
                ],
                acceptance=item.acceptance,
                depends_on=item.depends_on,
                max_retries=settings.max_task_retries,
            )
        )
    # Map depends_on deliverable ids -> task ids for runtime
    by_deliverable = {t.inputs["deliverable_id"]: t.id for t in tasks}
    for task in tasks:
        mapped: list[str] = []
        for dep in task.depends_on:
            if dep in by_deliverable:
                mapped.append(by_deliverable[dep])
            else:
                mapped.append(dep)
        task.depends_on = mapped
    return tasks


def _relevant(item: Any, text: str) -> bool:
    """Keep high-signal constraints in briefs without pasting the whole story bible."""
    terms = set((item.title + " " + item.acceptance + " " + item.layer).lower().split())
    words = set(text.lower().replace("/", " ").replace("–", " ").split())
    return len({word.strip(".,:;()[]") for word in terms & words if len(word) > 3}) >= 2


def create_tasks_if_approved(store: StudioStore, plan: ProductionPlan) -> list[Task]:
    if plan.status != PlanStatus.APPROVED:
        raise ApprovalRequiredError(
            f"Plan {plan.id} status is {plan.status.value}; approve before creating production tasks."
        )
    tasks = tasks_from_plan(plan, store.settings)
    # First wave with no deps becomes READY
    for task in tasks:
        if not task.depends_on:
            task.status = TaskStatus.READY
    return store.replace_plan_tasks(plan.id, tasks)


def _deps_satisfied(task: Task, all_tasks: dict[str, Task]) -> bool:
    for dep_id in task.depends_on:
        dep = all_tasks.get(dep_id)
        if dep is None or dep.status != TaskStatus.DONE:
            return False
    return True


def refresh_ready_states(store: StudioStore, plan_id: str) -> list[Task]:
    tasks = store.list_tasks(plan_id)
    by_id = {t.id: t for t in tasks}
    updated: list[Task] = []
    for task in tasks:
        if task.status in {TaskStatus.PENDING, TaskStatus.BLOCKED}:
            if _deps_satisfied(task, by_id):
                task.status = TaskStatus.READY
                store.save_task(task)
                updated.append(task)
            elif task.status == TaskStatus.PENDING and task.depends_on:
                task.status = TaskStatus.BLOCKED
                store.save_task(task)
    return updated


Handler = Callable[[Task], list[Evidence]]


def default_handler(task: Task, settings: Settings | None = None) -> list[Evidence]:
    """Deterministic stub handler that records a real on-disk receipt — not fake completion of game work."""
    from studio.config import ensure_project_dirs

    settings = ensure_project_dirs(settings)
    receipt_dir = settings.artifacts_dir / "task-receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt = receipt_dir / f"{task.id}.txt"
    receipt.write_text(
        (
            f"task_id={task.id}\n"
            f"title={task.title}\n"
            f"role={task.role}\n"
            f"acceptance={task.acceptance}\n"
            f"note=Studio scheduled this production task. "
            f"Game deliverable itself is NOT claimed complete.\n"
            f"updated={utc_now().isoformat()}\n"
        ),
        encoding="utf-8",
    )
    return [
        Evidence(
            kind="receipt",
            reference=str(receipt.relative_to(settings.repo_root)),
            detail="Scheduling receipt only; gameplay/art output still pending human/agent production work.",
        )
    ]


def run_task(
    store: StudioStore,
    task_id: str,
    *,
    handler: Handler | None = None,
    require_approved_plan: bool = True,
) -> Task:
    task = store.get_task(task_id)
    if task is None:
        raise KeyError(f"Unknown task: {task_id}")

    plan = store.get_plan(task.plan_id)
    if plan is None:
        raise KeyError(f"Missing plan for task: {task.plan_id}")
    if require_approved_plan and plan.status != PlanStatus.APPROVED:
        raise ApprovalRequiredError(
            f"Refusing to run task {task_id}: plan not approved ({plan.status.value})."
        )

    all_tasks = {t.id: t for t in store.list_tasks(task.plan_id)}
    if not _deps_satisfied(task, all_tasks):
        task.status = TaskStatus.BLOCKED
        task.error = "Dependencies not done"
        store.save_task(task)
        raise TaskExecutionError(task.error)

    if handler is None:
        from studio.agents import production_agent_handler

        handler = lambda t: production_agent_handler(t, store.settings, store)

    while True:
        task.status = TaskStatus.RUNNING
        task.error = None
        store.save_task(task)
        try:
            evidence = handler(task)
            if not evidence:
                raise TaskExecutionError("Handler returned no evidence")
            task.evidence = evidence
            task.outputs.update({
                "evidence_count": len(evidence),
                "references": [e.reference for e in evidence],
            })
            task.status = TaskStatus.DONE
            store.save_task(task)
            refresh_ready_states(store, task.plan_id)
            store.log_event("task_done", {"task_id": task.id})
            return task
        except Exception as exc:  # noqa: BLE001 — persist, retry, then fail
            task.retries += 1
            task.error = str(exc)
            if task.retries <= task.max_retries:
                task.status = TaskStatus.READY
                store.save_task(task)
                store.log_event(
                    "task_retry",
                    {
                        "task_id": task.id,
                        "retries": task.retries,
                        "error": str(exc),
                    },
                )
                continue
            task.status = TaskStatus.FAILED
            store.save_task(task)
            store.log_event("task_failed", {"task_id": task.id, "error": str(exc)})
            raise


def run_ready_tasks(
    store: StudioStore,
    plan_id: str,
    *,
    limit: int = 10,
    handler: Handler | None = None,
) -> list[Task]:
    refresh_ready_states(store, plan_id)
    completed: list[Task] = []
    for task in store.list_tasks(plan_id):
        if task.status != TaskStatus.READY:
            continue
        if len(completed) >= limit:
            break
        completed.append(run_task(store, task.id, handler=handler))
    return completed


def task_counts(tasks: list[Task]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for task in tasks:
        counts[task.status.value] = counts.get(task.status.value, 0) + 1
    return counts
