"""CLI entrypoint: python -m studio.cli ..."""

from __future__ import annotations

import json
from typing import Optional

import typer
from rich import print as rprint

from studio import service

app = typer.Typer(help="Rad-e Hoor AI game studio CLI", no_args_is_help=True)


@app.command("align")
def align_cmd() -> None:
    """Ingest gameStory, write analysis + draft production plan."""
    result = service.bootstrap_alignment()
    rprint(result)


@app.command("status")
def status_cmd() -> None:
    """Show studio phase, plan, and task counts."""
    status = service.get_status()
    rprint(status.model_dump())


@app.command("submit")
def submit_cmd() -> None:
    """Submit latest plan for human approval."""
    rprint(service.submit_latest())


@app.command("approve")
def approve_cmd(
    note: str = typer.Option("Approved by human", "--note", "-n"),
) -> None:
    """Approve latest plan and create executable tasks."""
    rprint(service.approve_latest(note=note))


@app.command("reject")
def reject_cmd(
    note: str = typer.Option("Rejected by human", "--note", "-n"),
) -> None:
    """Reject latest plan."""
    rprint(service.reject_latest(note=note))


@app.command("tasks")
def tasks_cmd(plan_id: Optional[str] = typer.Option(None, "--plan-id")) -> None:
    """List tasks for a plan (default: latest)."""
    store = service.StudioStore()
    plan = store.get_plan(plan_id) if plan_id else store.latest_plan()
    if plan is None:
        rprint({"error": "no plan"})
        raise typer.Exit(code=1)
    tasks = store.list_tasks(plan.id)
    rprint(
        [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status.value,
                "role": t.role,
                "retries": t.retries,
            }
            for t in tasks
        ]
    )


@app.command("run")
def run_cmd(limit: int = typer.Option(5, "--limit", "-l")) -> None:
    """Run ready production tasks (requires approved plan)."""
    rprint(service.run_batch(limit=limit))


@app.command("serve")
def serve_cmd(
    host: str = "127.0.0.1",
    port: int = 8000,
) -> None:
    """Run local HTTP API."""
    import uvicorn

    uvicorn.run("studio.api:app", host=host, port=port, reload=False)


@app.command("dump-json")
def dump_json_cmd() -> None:
    """Print status as JSON (script-friendly)."""
    print(json.dumps(service.get_status().model_dump(mode="json"), indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
