"""Pydantic domain models for studio state."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TaskStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    DONE = "done"
    FAILED = "failed"


class PlanStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class Phase(str, Enum):
    A_ALIGNMENT = "A_alignment"
    B_STUDIO = "B_studio"
    C_PRODUCTION = "C_production"


class StoryDocument(BaseModel):
    path: str
    title: str
    sha256: str
    size_bytes: int
    mtime_iso: str
    headings: list[str] = Field(default_factory=list)
    summary: str = ""
    is_historical: bool = False


class StoryIndex(BaseModel):
    project_id: str
    generated_at: datetime = Field(default_factory=utc_now)
    root: str
    documents: list[StoryDocument] = Field(default_factory=list)
    missing: bool = False
    notes: list[str] = Field(default_factory=list)


class Assumption(BaseModel):
    id: str
    text: str
    source: str | None = None


class ApprovedFact(BaseModel):
    id: str
    text: str
    source: str


class StoryAnalysis(BaseModel):
    project_id: str
    generated_at: datetime = Field(default_factory=utc_now)
    concept: str
    genre: str
    platform: str
    campaign_time_budget_minutes: int
    gameplay_loop: str
    hearing_notes: list[str] = Field(default_factory=list)
    chapter_structure: list[str] = Field(default_factory=list)
    characters: list[str] = Field(default_factory=list)
    prohibitions: list[str] = Field(default_factory=list)
    audio_accessibility: list[str] = Field(default_factory=list)
    technical_risks: list[str] = Field(default_factory=list)
    open_gaps: list[str] = Field(default_factory=list)
    approved: list[ApprovedFact] = Field(default_factory=list)
    assumptions: list[Assumption] = Field(default_factory=list)
    source_paths: list[str] = Field(default_factory=list)
    markdown_path: str | None = None


class PlanDeliverable(BaseModel):
    id: str
    title: str
    layer: str
    acceptance: str
    depends_on: list[str] = Field(default_factory=list)
    agent_role: str


class ProductionPlan(BaseModel):
    id: str
    project_id: str
    status: PlanStatus = PlanStatus.DRAFT
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    summary: str
    phases: list[str] = Field(default_factory=list)
    deliverables: list[PlanDeliverable] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    human_gates: list[str] = Field(default_factory=list)
    markdown_path: str | None = None
    approval_note: str | None = None
    approved_at: datetime | None = None


class Evidence(BaseModel):
    kind: str
    reference: str
    detail: str | None = None


class Task(BaseModel):
    id: str
    plan_id: str
    title: str
    role: str
    status: TaskStatus = TaskStatus.PENDING
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, Any] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)
    acceptance: str
    depends_on: list[str] = Field(default_factory=list)
    retries: int = 0
    max_retries: int = 3
    error: str | None = None
    evidence: list[Evidence] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class StudioStatus(BaseModel):
    project_id: str
    phase: Phase
    game_story_present: bool
    document_count: int
    plan_id: str | None
    plan_status: PlanStatus | None
    task_counts: dict[str, int] = Field(default_factory=dict)
    analysis_path: str | None = None
    plan_path: str | None = None
