"""Embedded SQLite persistence for plans, tasks, and approvals.

Uses a local file under `projects/<id>/data/studio.db`.
No database server install or daemon is required — SQLite ships with Python.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from studio.config import Settings, ensure_project_dirs
from studio.models import (
    Evidence,
    PlanStatus,
    ProductionPlan,
    Task,
    TaskStatus,
    utc_now,
)


class Base(DeclarativeBase):
    pass


class PlanRow(Base):
    __tablename__ = "plans"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32))
    payload_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TaskRow(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    plan_id: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    payload_json: Mapped[str] = mapped_column(Text)
    retries: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ApprovalRow(Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_id: Mapped[str] = mapped_column(String(64), index=True)
    decision: Mapped[str] = mapped_column(String(32))
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class EventRow(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kind: Mapped[str] = mapped_column(String(64))
    payload_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class StudioStore:
    """File-backed store. Path: `settings.db_path` (SQLite)."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = ensure_project_dirs(settings)
        # Embedded SQLite only — no Postgres/MySQL server.
        url = f"sqlite:///{self.settings.db_path}"
        self.engine = create_engine(
            url,
            future=True,
            connect_args={"check_same_thread": False},
        )
        Base.metadata.create_all(self.engine)
        self._session_factory = sessionmaker(self.engine, expire_on_commit=False)

    def session(self) -> Session:
        return self._session_factory()

    def log_event(self, kind: str, payload: dict[str, Any]) -> None:
        with self.session() as session:
            session.add(
                EventRow(
                    kind=kind,
                    payload_json=json.dumps(payload, default=str),
                    created_at=utc_now(),
                )
            )
            session.commit()

    def save_plan(self, plan: ProductionPlan) -> ProductionPlan:
        plan.updated_at = utc_now()
        with self.session() as session:
            row = session.get(PlanRow, plan.id)
            payload = plan.model_dump(mode="json")
            if row is None:
                session.add(
                    PlanRow(
                        id=plan.id,
                        project_id=plan.project_id,
                        status=plan.status.value,
                        payload_json=json.dumps(payload),
                        created_at=plan.created_at,
                        updated_at=plan.updated_at,
                    )
                )
            else:
                row.status = plan.status.value
                row.payload_json = json.dumps(payload)
                row.updated_at = plan.updated_at
            session.commit()
        self.log_event("plan_saved", {"plan_id": plan.id, "status": plan.status.value})
        return plan

    def get_plan(self, plan_id: str) -> ProductionPlan | None:
        with self.session() as session:
            row = session.get(PlanRow, plan_id)
            if row is None:
                return None
            return ProductionPlan.model_validate_json(row.payload_json)

    def latest_plan(self, project_id: str | None = None) -> ProductionPlan | None:
        project_id = project_id or self.settings.project_id
        with self.session() as session:
            stmt = (
                select(PlanRow)
                .where(PlanRow.project_id == project_id)
                .order_by(PlanRow.updated_at.desc())
                .limit(1)
            )
            row = session.scalars(stmt).first()
            if row is None:
                return None
            return ProductionPlan.model_validate_json(row.payload_json)

    def list_plans(self, project_id: str | None = None) -> list[ProductionPlan]:
        project_id = project_id or self.settings.project_id
        with self.session() as session:
            stmt = (
                select(PlanRow)
                .where(PlanRow.project_id == project_id)
                .order_by(PlanRow.updated_at.desc())
            )
            return [
                ProductionPlan.model_validate_json(row.payload_json)
                for row in session.scalars(stmt).all()
            ]

    def record_approval(self, plan_id: str, decision: str, note: str = "") -> None:
        with self.session() as session:
            session.add(
                ApprovalRow(
                    plan_id=plan_id,
                    decision=decision,
                    note=note,
                    created_at=utc_now(),
                )
            )
            session.commit()
        self.log_event(
            "approval",
            {"plan_id": plan_id, "decision": decision, "note": note},
        )

    def save_task(self, task: Task) -> Task:
        task.updated_at = utc_now()
        with self.session() as session:
            row = session.get(TaskRow, task.id)
            payload = task.model_dump(mode="json")
            if row is None:
                session.add(
                    TaskRow(
                        id=task.id,
                        plan_id=task.plan_id,
                        status=task.status.value,
                        payload_json=json.dumps(payload),
                        retries=task.retries,
                        updated_at=task.updated_at,
                    )
                )
            else:
                row.status = task.status.value
                row.payload_json = json.dumps(payload)
                row.retries = task.retries
                row.updated_at = task.updated_at
            session.commit()
        return task

    def get_task(self, task_id: str) -> Task | None:
        with self.session() as session:
            row = session.get(TaskRow, task_id)
            if row is None:
                return None
            return Task.model_validate_json(row.payload_json)

    def list_tasks(self, plan_id: str | None = None) -> list[Task]:
        with self.session() as session:
            stmt = select(TaskRow)
            if plan_id:
                stmt = stmt.where(TaskRow.plan_id == plan_id)
            stmt = stmt.order_by(TaskRow.updated_at.asc())
            return [
                Task.model_validate_json(row.payload_json)
                for row in session.scalars(stmt).all()
            ]

    def replace_plan_tasks(self, plan_id: str, tasks: list[Task]) -> list[Task]:
        with self.session() as session:
            existing = session.scalars(
                select(TaskRow).where(TaskRow.plan_id == plan_id)
            ).all()
            for row in existing:
                session.delete(row)
            session.commit()
        saved: list[Task] = []
        for task in tasks:
            saved.append(self.save_task(task))
        self.log_event(
            "tasks_replaced",
            {"plan_id": plan_id, "count": len(saved)},
        )
        return saved


def evidence_dict(evidence: list[Evidence]) -> list[dict[str, Any]]:
    return [item.model_dump() for item in evidence]
