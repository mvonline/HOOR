# Studio UI (Streamlit)

Simple control panel for the Rad-e Hoor studio. Lives in `ui/` so it stays separate from `studio/` core logic.

## Run

From the repository root, with the project venv active:

```bash
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
streamlit run ui/app.py
```

Opens a local browser UI (default `http://localhost:8501`).

## What it does

- **Plan tab** — view the full production plan, edit summary/phases/deliverables/risks/gates, then **Save / Submit / Approve / Reject**
- **Align** — ingest `gameStory/`, write a new draft plan (supersedes previous)
- **Run ready tasks** — execute specialist implementation and independent review; requires a configured AI provider
- View tasks, status, and analysis

Editing an **approved** plan resets it to **draft** and requires re-approval.

Persistence remains embedded SQLite at `projects/rade-hoor/data/studio.db`.
