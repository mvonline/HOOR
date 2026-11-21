"""Collaborative, file-producing AI agent runtime for approved studio tasks.

The runtime uses an OpenAI-compatible chat completions endpoint. Agents return
structured file proposals; only paths inside the game workspace and the current
plan's artifact folder can be written.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import httpx

from studio.config import Settings, ensure_project_dirs
from studio.db import StudioStore
from studio.models import Evidence, PlanDeliverable, Task


class AgentRuntimeError(RuntimeError):
    pass


def suggest_breakdown(goal: str, constraints: str, settings: Settings) -> list[PlanDeliverable]:
    """Ask the production manager agent to propose reviewable, dependency-aware work."""
    if not goal.strip():
        raise AgentRuntimeError("Describe the outcome before requesting a task breakdown.")
    analysis_path = settings.analysis_dir / "story-analysis.json"
    analysis = analysis_path.read_text(encoding="utf-8")[:24000] if analysis_path.exists() else ""
    prompt = (
        "You are the production manager for Rad-e Hoor. Break the user's requested outcome into "
        "small implementation deliverables an engineering team can complete and review. Respect "
        "the supplied approved analysis, do not invent story content, label unresolved guesses as "
        "assumptions, keep work playable and incremental, and include acceptance criteria that can "
        "be checked from files or a build. Return JSON: {deliverables:[{id,title,layer,acceptance,"
        "depends_on:[ids],agent_role}], risks:[strings], questions:[strings]}. Use unique IDs, "
        "dependencies only among proposed deliverables, 2-8 tasks, and use roles such as Gameplay "
        "Engineer, Audio Director, QA / Playtest Lead, Narrative Lead, Technical Director."
    )
    raw = _request(settings, [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"GOAL\n{goal}\n\nUSER CONSTRAINTS\n{constraints}\n\nAPPROVED STORY ANALYSIS\n{analysis}"},
    ])
    result = _json_object(raw)
    raw_items = result.get("deliverables")
    if not isinstance(raw_items, list) or not 2 <= len(raw_items) <= 8:
        raise AgentRuntimeError("Planner must return between 2 and 8 deliverables.")
    try:
        deliverables = [PlanDeliverable.model_validate(item) for item in raw_items]
    except Exception as exc:
        raise AgentRuntimeError(f"Planner returned invalid deliverables: {exc}") from exc
    ids = [item.id for item in deliverables]
    if len(ids) != len(set(ids)):
        raise AgentRuntimeError("Planner returned duplicate deliverable IDs.")
    known = set(ids)
    if any(dep not in known for item in deliverables for dep in item.depends_on):
        raise AgentRuntimeError("Planner dependencies must reference proposed deliverable IDs.")
    pending = {item.id: set(item.depends_on) for item in deliverables}
    resolved: set[str] = set()
    while pending:
        ready = {item_id for item_id, deps in pending.items() if deps <= resolved}
        if not ready:
            raise AgentRuntimeError("Planner returned cyclic task dependencies.")
        resolved.update(ready)
        for item_id in ready:
            pending.pop(item_id)
    return deliverables


ROLE_GUIDANCE = {
    "gameplay engineer": "Implement playable systems and interactions with clear controls and feedback.",
    "game designer": "Implement and tune the player-facing rules, flow, and choices.",
    "audio director": "Implement sound behavior, spatial cues, and accessible non-audio alternatives.",
    "qa / playtest lead": "Build instrumentation, reproducible checks, and facilitator-facing outputs.",
    "technical director": "Implement architecture and tooling needed by this deliverable.",
    "narrative lead": "Integrate only approved story content and preserve source voice and continuity.",
    "studio manager": "Produce evidence-based production decisions and unblock the next approved step.",
    "independent reviewer": "Review the actual files against the work order and design constraints.",
}


def _request(settings: Settings, messages: list[dict[str, str]], *, json_mode: bool = True) -> str:
    if not settings.ai_api_key and "localhost" not in settings.ai_base_url and "127.0.0.1" not in settings.ai_base_url:
        raise AgentRuntimeError(
            "AI provider is not configured. Set STUDIO_AI_API_KEY, STUDIO_AI_MODEL, "
            "and optionally STUDIO_AI_BASE_URL (OpenAI-compatible endpoint)."
        )
    headers = {"Content-Type": "application/json"}
    if settings.ai_api_key:
        headers["Authorization"] = f"Bearer {settings.ai_api_key}"
    payload: dict[str, Any] = {
        "model": settings.ai_model,
        "messages": messages,
        "temperature": 0.2,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    url = settings.ai_base_url.rstrip("/") + "/chat/completions"
    try:
        response = httpx.post(
            url, headers=headers, json=payload, timeout=settings.ai_timeout_seconds
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
        raise AgentRuntimeError(f"AI provider request failed: {exc}") from exc


def _json_object(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AgentRuntimeError(f"Agent returned invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise AgentRuntimeError("Agent response must be a JSON object")
    return value


def _read_context(task: Task, settings: Settings, store: StudioStore) -> tuple[str, list[dict[str, str]]]:
    pieces: list[str] = []
    work_order = task.inputs.get("work_order")
    if work_order:
        path = (settings.repo_root / work_order).resolve()
        if path.is_file() and path.is_relative_to(settings.repo_root.resolve()):
            pieces.append(f"## Approved work order\n{path.read_text(encoding='utf-8')}")
    sources = task.inputs.get("source_documents", [])
    for relative in sources:
        path = (settings.repo_root / relative).resolve()
        if path.is_file() and path.is_relative_to(settings.game_story_dir.resolve()):
            text = path.read_text(encoding="utf-8", errors="replace")
            pieces.append(f"## Source: {relative}\n{text[:12000]}")
    game_dir = settings.repo_root / "game"
    if game_dir.exists():
        state: list[str] = []
        total = 0
        for path in sorted(p for p in game_dir.rglob("*") if p.is_file()):
            rel = path.relative_to(settings.repo_root).as_posix()
            try:
                body = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                state.append(f"- `{rel}` (binary/unreadable; preserved)")
                continue
            state.append(f"## Existing file: {rel}\n```\n{body[:6000]}\n```")
            total += len(body)
            if total >= 30000 or len(state) >= 30:
                break
        if state:
            pieces.append("## Existing game workspace (inspect and extend; preserve unrelated files)\n" + "\n\n".join(state))
    collaborators: list[dict[str, str]] = []
    for dep_id in task.depends_on:
        dep = store.get_task(dep_id)
        if dep:
            report = dep.outputs.get("agent_report")
            collaborators.append({
                "task": dep.title,
                "report": str(report or "No report recorded"),
                "files": ", ".join(dep.outputs.get("changed_files", [])),
            })
    if collaborators:
        pieces.append("## Upstream agent handoffs\n" + json.dumps(collaborators, indent=2))
    # Keep request bounded; sources are supplied in the work order and should remain focused.
    context = "\n\n".join(pieces)
    return context[:55000], collaborators


def _validate_file_path(raw: str, settings: Settings, task: Task) -> Path:
    relative = Path(raw.replace("\\", "/"))
    if relative.is_absolute() or ".." in relative.parts:
        raise AgentRuntimeError(f"Agent proposed unsafe path: {raw}")
    allowed_artifacts = Path("projects") / settings.project_id / "artifacts" / "agent-output" / task.plan_id
    if not (relative.parts and relative.parts[0] == "game") and not relative.is_relative_to(allowed_artifacts):
        raise AgentRuntimeError(f"Agent may only write under game/ or {allowed_artifacts}: {raw}")
    destination = (settings.repo_root / relative).resolve()
    if not destination.is_relative_to(settings.repo_root.resolve()):
        raise AgentRuntimeError(f"Agent path escapes repository: {raw}")
    return destination


def _write_proposal(files: list[dict[str, Any]], settings: Settings, task: Task) -> list[str]:
    if not files:
        raise AgentRuntimeError("Implementer returned no files")
    validated: list[tuple[Path, str]] = []
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("content"), str):
            raise AgentRuntimeError("Each proposed file must contain string path and content fields")
        destination = _validate_file_path(item["path"], settings, task)
        validated.append((destination, item["content"]))
    changed: list[str] = []
    for destination, content in validated:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        changed.append(destination.relative_to(settings.repo_root).as_posix())
    return changed


def _snapshot(paths: list[str], settings: Settings) -> str:
    files = []
    for relative in paths:
        path = settings.repo_root / relative
        files.append({"path": relative, "content": path.read_text(encoding="utf-8")})
    return json.dumps(files, ensure_ascii=False)


def production_agent_handler(task: Task, settings: Settings, store: StudioStore) -> list[Evidence]:
    """Run specialist implementation, peer review, and one revision cycle."""
    settings = ensure_project_dirs(settings)
    context, _ = _read_context(task, settings, store)
    role = task.role.lower()
    guidance = next((value for key, value in ROLE_GUIDANCE.items() if key in role),
                    "Implement the approved deliverable using your specialist judgment.")
    system = (
        "You are a production agent in the Rad-e Hoor game studio. Implement the approved task "
        "in the shared game repository. Follow the work order and cited source truth. Never modify "
        "gameStory/. Do not invent approved story facts. Return JSON only with keys: summary, "
        "files (array of {path, content}), acceptance_evidence (array of strings), assumptions "
        "(array). Use complete file contents for every changed file. Keep the build runnable.\n\n"
        f"Your discipline: {guidance}"
    )
    user = f"TASK\n{task.title}\n\nACCEPTANCE\n{task.acceptance}\n\nCONTEXT\n{context}"
    implementation = _json_object(_request(settings, [
        {"role": "system", "content": system}, {"role": "user", "content": user}
    ]))
    changed = _write_proposal(implementation.get("files", []), settings, task)
    reviewer_system = (
        "You are an independent reviewer in a game studio. Review the proposed implementation "
        "against the work order, acceptance criteria, and design sources. Check completeness, "
        "story constraints, obvious runtime defects, accessibility, and privacy where relevant. "
        "Return JSON only: {approved: boolean, issues: [strings], summary: string}. Approve only "
        "when the acceptance criteria are addressed by concrete files."
    )
    review = _json_object(_request(settings, [
        {"role": "system", "content": reviewer_system},
        {"role": "user", "content": f"{user}\n\nPROPOSED IMPLEMENTATION FILES\n{_snapshot(changed, settings)}\n\nIMPLEMENTER SUMMARY\n{implementation.get('summary', '')}"},
    ]))
    if review.get("approved") is not True:
        revision = _json_object(_request(settings, [
            {"role": "system", "content": system},
            {"role": "user", "content": f"{user}\n\nPEER REVIEW FEEDBACK\n{json.dumps(review, ensure_ascii=False)}\n\nRevise the implementation to resolve valid issues."},
        ]))
        revised_paths = _write_proposal(revision.get("files", []), settings, task)
        changed = list(dict.fromkeys(changed + revised_paths))
        implementation = revision
        review = _json_object(_request(settings, [
            {"role": "system", "content": reviewer_system},
            {"role": "user", "content": f"{user}\n\nREVISED IMPLEMENTATION FILES\n{_snapshot(changed, settings)}\n\nIMPLEMENTER SUMMARY\n{revision.get('summary', '')}"},
        ]))
    if review.get("approved") is not True:
        raise AgentRuntimeError("Peer review rejected the implementation: " + "; ".join(map(str, review.get("issues", []))))

    report_dir = settings.artifacts_dir / "agent-output" / task.plan_id
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{re.sub(r'[^a-zA-Z0-9_-]+', '-', task.inputs.get('deliverable_id', task.id))}-report.md"
    report_path.write_text(
        "# Agent production report\n\n"
        f"- Task: {task.title}\n- Specialist: {task.role}\n- Peer review: approved\n\n"
        f"## Implementation\n{implementation.get('summary', '')}\n\n"
        f"## Acceptance evidence\n" + "\n".join(f"- {x}" for x in implementation.get("acceptance_evidence", [])) +
        "\n\n## Assumptions\n" + "\n".join(f"- {x}" for x in implementation.get("assumptions", [])) +
        "\n\n## Reviewer\n" + str(review.get("summary", "Approved")) +
        "\n\n## Files\n" + "\n".join(f"- `{path}`" for path in changed) + "\n",
        encoding="utf-8",
    )
    task.outputs.update({"changed_files": changed, "agent_report": report_path.relative_to(settings.repo_root).as_posix()})
    return [
        Evidence(kind="implementation", reference=path, detail="File produced by specialist agent")
        for path in changed
    ] + [Evidence(kind="peer_review", reference=report_path.relative_to(settings.repo_root).as_posix(), detail="Independent reviewer approved the implementation")]
