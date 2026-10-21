"""Streamlit UI for the Rad-e Hoor studio — plan view, edit, approve.

Run from repo root (with venv active):

    streamlit run ui/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from studio import service  # noqa: E402
from studio.config import get_settings  # noqa: E402
from studio.db import StudioStore  # noqa: E402
from studio.models import PlanStatus  # noqa: E402

st.set_page_config(
    page_title="Rad-e Hoor Studio",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _load_text(rel: str | None) -> str | None:
    if not rel:
        return None
    path = REPO_ROOT / rel
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def _lines_to_text(items: list[str]) -> str:
    return "\n".join(items)


def _text_to_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _deliverables_frame(plan) -> pd.DataFrame:
    rows = []
    for d in plan.deliverables:
        rows.append(
            {
                "id": d.id,
                "layer": d.layer,
                "title": d.title,
                "agent_role": d.agent_role,
                "depends_on": ", ".join(d.depends_on),
                "acceptance": d.acceptance,
            }
        )
    return pd.DataFrame(rows)


def _render_plan_tab(store: StudioStore, plan, note: str) -> None:
    if plan is None:
        st.warning("No plan yet. Use **Align** in the sidebar to generate a draft.")
        return

    status_color = {
        PlanStatus.DRAFT: "orange",
        PlanStatus.PENDING_APPROVAL: "blue",
        PlanStatus.APPROVED: "green",
        PlanStatus.REJECTED: "red",
        PlanStatus.SUPERSEDED: "gray",
    }.get(plan.status, "gray")

    st.markdown(
        f"**Plan ID:** `{plan.id}` &nbsp;|&nbsp; "
        f"**Status:** :{status_color}[**{plan.status.value}**]"
    )
    if plan.approval_note:
        st.caption(f"Last note: {plan.approval_note}")

    st.info(
        "Edit fields below, then **Save edits**. "
        "Saving an approved plan resets it to **draft** (you must approve again). "
        "Then **Submit** → **Approve**."
    )

    # —— Approval actions on the plan page ——
    a1, a2, a3, a4 = st.columns([1, 1, 1, 2])
    with a1:
        if st.button("Save edits", type="primary", use_container_width=True):
            st.session_state["_save_plan"] = True
    with a2:
        if st.button("Submit", use_container_width=True):
            try:
                result = service.submit_latest(store)
                (st.info if result.get("unchanged") else st.success)(
                    result.get("message", result)
                )
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))
    with a3:
        if st.button("Approve", use_container_width=True):
            try:
                result = service.approve_latest(note=note, store=store)
                (st.info if result.get("unchanged") else st.success)(
                    result.get("message", result)
                )
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))
    with a4:
        if st.button("Reject", use_container_width=True):
            try:
                result = service.reject_latest(note=note, store=store)
                st.warning(result)
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))

    st.divider()

    summary = st.text_area("Summary", value=plan.summary, height=120, key="plan_summary")
    phases = st.text_area(
        "Phases (one per line)",
        value=_lines_to_text(plan.phases),
        height=140,
        key="plan_phases",
    )

    st.subheader("Deliverables")
    st.caption(
        "Edit cells directly. `depends_on` = comma-separated deliverable ids. "
        "Add/remove rows with the table toolbar."
    )
    edited = st.data_editor(
        _deliverables_frame(plan),
        num_rows="dynamic",
        use_container_width=True,
        height=420,
        key="plan_deliverables_editor",
        column_config={
            "id": st.column_config.TextColumn("id", required=True, width="medium"),
            "layer": st.column_config.TextColumn("layer", width="small"),
            "title": st.column_config.TextColumn("title", width="large"),
            "agent_role": st.column_config.TextColumn("agent_role", width="medium"),
            "depends_on": st.column_config.TextColumn("depends_on", width="medium"),
            "acceptance": st.column_config.TextColumn("acceptance", width="large"),
        },
    )

    risks = st.text_area(
        "Risks (one per line)",
        value=_lines_to_text(plan.risks),
        height=120,
        key="plan_risks",
    )
    gates = st.text_area(
        "Human gates (one per line)",
        value=_lines_to_text(plan.human_gates),
        height=120,
        key="plan_gates",
    )

    with st.expander("Markdown preview (read-only file)"):
        text = _load_text(plan.markdown_path)
        if text:
            st.markdown(text)
        else:
            st.write("No markdown file yet — Save edits to write it.")

    if st.session_state.pop("_save_plan", False):
        try:
            rows = edited.fillna("").to_dict(orient="records")
            result = service.save_plan_edits(
                plan,
                summary=summary,
                phases=_text_to_lines(phases),
                risks=_text_to_lines(risks),
                human_gates=_text_to_lines(gates),
                deliverables=rows,
                store=store,
            )
            st.success(result["message"])
            st.rerun()
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))


def main() -> None:
    st.title("Rad-e Hoor — Studio")
    st.caption(
        "Plan is editable and approvable here. "
        "`gameStory/` remains the design source of truth (read-only)."
    )

    settings = get_settings()
    store = StudioStore(settings)

    with st.sidebar:
        st.header("Studio actions")
        note = st.text_input("Approval / reject note", value="Approved by human")
        run_limit = st.number_input("Run batch limit", min_value=1, max_value=20, value=3)

        if st.button("Align (regenerate draft plan)", type="primary"):
            with st.spinner("Running alignment…"):
                result = service.bootstrap_alignment(settings)
            st.success(f"New draft: `{result['plan_id']}`")
            st.rerun()

        if st.button("Run ready tasks"):
            try:
                result = service.run_batch(limit=int(run_limit), store=store)
                st.success(f"Ran: {result.get('ran', [])}")
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))

        st.divider()
        st.caption(f"SQLite: `{settings.db_path.relative_to(REPO_ROOT)}`")
        if st.button("Refresh"):
            st.rerun()

    status = service.get_status(settings)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Phase", status.phase.value)
    c2.metric("Plan status", status.plan_status.value if status.plan_status else "—")
    c3.metric("Documents", status.document_count)
    c4.metric("Story present", "yes" if status.game_story_present else "no")

    plan = store.latest_plan()
    tasks = store.list_tasks(plan.id) if plan else []

    tab_plan, tab_tasks, tab_status, tab_analysis = st.tabs(
        ["Plan (edit & approve)", "Tasks", "Status", "Analysis"]
    )

    with tab_plan:
        _render_plan_tab(store, plan, note)

    with tab_tasks:
        if status.task_counts:
            st.json(status.task_counts)
        if not tasks:
            st.info("No tasks yet. Approve the plan to create them.")
        else:
            st.dataframe(
                [
                    {
                        "id": t.id,
                        "title": t.title,
                        "status": t.status.value,
                        "role": t.role,
                        "retries": t.retries,
                        "layer": t.inputs.get("layer"),
                    }
                    for t in tasks
                ],
                use_container_width=True,
            )

    with tab_status:
        st.write(
            {
                "project_id": status.project_id,
                "plan_id": status.plan_id,
                "analysis_path": status.analysis_path,
                "plan_path": status.plan_path,
                "task_counts": status.task_counts,
            }
        )

    with tab_analysis:
        text = _load_text(status.analysis_path)
        if text:
            st.markdown(text)
        else:
            st.warning("No analysis yet. Click Align.")


if __name__ == "__main__":
    main()
