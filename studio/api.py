"""Local HTTP API for plan/task status."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from studio import service
from studio.db import StudioStore
from studio.models import StudioStatus

app = FastAPI(
    title="Rad-e Hoor Studio API",
    version="0.1.0",
    description="AI-native multi-agent game studio status and control surface",
)


class NoteBody(BaseModel):
    note: str = Field(default="Approved by human")


class RunBody(BaseModel):
    limit: int = Field(default=5, ge=1, le=50)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "service": "rade-hoor-studio"}


@app.get("/status", response_model=StudioStatus)
def status() -> StudioStatus:
    return service.get_status()


@app.post("/align")
def align() -> dict:
    return service.bootstrap_alignment()


@app.post("/plans/submit")
def submit() -> dict:
    try:
        return service.submit_latest()
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/plans/approve")
def approve(body: NoteBody) -> dict:
    try:
        return service.approve_latest(note=body.note)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/plans/reject")
def reject(body: NoteBody) -> dict:
    try:
        return service.reject_latest(note=body.note)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/plans/latest")
def latest_plan() -> dict:
    store = StudioStore()
    plan = store.latest_plan()
    if plan is None:
        raise HTTPException(status_code=404, detail="No plan")
    return plan.model_dump(mode="json")


@app.get("/tasks")
def list_tasks() -> list[dict]:
    store = StudioStore()
    plan = store.latest_plan()
    if plan is None:
        return []
    return [t.model_dump(mode="json") for t in store.list_tasks(plan.id)]


@app.post("/tasks/run")
def run_tasks(body: RunBody) -> dict:
    try:
        return service.run_batch(limit=body.limit)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
